#!/usr/bin/env python3
"""
MarkHub v5.0 - 智能 ComfyUI 远程控制系统

核心功能：
- 自动读取工作流
- 自动选择模型和工作流
- 智能搜索最佳实践
- 自动生成图片和视频
- 参数自动优化
"""

import requests
import json
import uuid
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib.request
import urllib.parse
import ssl

# 忽略 SSL 证书验证
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class ComfyUIRemote:
    """智能 ComfyUI 远程客户端"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client_id = str(uuid.uuid4())
        self.session = requests.Session()
        self.session.verify = False
        self.object_info = None
        self.workflows = None
        
    def get_object_info(self, force_refresh: bool = False) -> Dict:
        """获取节点信息"""
        if self.object_info and not force_refresh:
            return self.object_info
        
        try:
            print(f"📚 获取节点信息...")
            resp = self.session.get(f"{self.base_url}/object_info", timeout=30)
            self.object_info = resp.json()
            print(f"✅ 获取到 {len(self.object_info)} 个节点")
            return self.object_info
        except Exception as e:
            print(f"❌ 获取节点信息失败：{e}")
            return {}
    
    def get_queue(self) -> Dict:
        """获取队列状态"""
        try:
            resp = self.session.get(f"{self.base_url}/queue", timeout=10)
            return resp.json()
        except Exception as e:
            print(f"获取队列失败：{e}")
            return {}
    
    def get_history(self, prompt_id: str) -> Dict:
        """获取生成历史"""
        try:
            resp = self.session.get(f"{self.base_url}/history/{prompt_id}", timeout=10)
            return resp.json()
        except Exception as e:
            return {}
    
    def queue_prompt(self, prompt: Dict) -> Optional[Dict]:
        """提交提示词"""
        try:
            payload = {
                "prompt": prompt,
                "client_id": self.client_id
            }
            resp = self.session.post(
                f"{self.base_url}/prompt",
                json=payload,
                timeout=30
            )
            return resp.json()
        except Exception as e:
            print(f"提交失败：{e}")
            return None
    
    def upload_image(self, image_path: str) -> Optional[Dict]:
        """上传图片"""
        try:
            with open(image_path, 'rb') as f:
                files = {
                    'image': (Path(image_path).name, f, 'image/png')
                }
                data = {'overwrite': 'true'}
                resp = self.session.post(
                    f"{self.base_url}/upload/image",
                    files=files,
                    data=data,
                    timeout=30
                )
                return resp.json()
        except Exception as e:
            print(f"上传图片失败：{e}")
            return None
    
    def download_file(self, filename: str, output_dir: str, subfolder: str = "") -> Optional[str]:
        """下载生成的文件"""
        try:
            params = {
                "filename": filename,
                "subfolder": subfolder,
                "type": "output"
            }
            url = f"{self.base_url}/view?{urllib.parse.urlencode(params)}"
            
            output_path = Path(output_dir) / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with self.session.get(url, stream=True) as resp:
                resp.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            return str(output_path)
        except Exception as e:
            print(f"下载失败：{e}")
            return None
    
    def wait_for_prompt(self, prompt_id: str, timeout: int = 600) -> Optional[Dict]:
        """等待生成完成"""
        start_time = time.time()
        print(f"⏳ 等待生成完成...（超时：{timeout}秒）")
        
        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)
            if history and prompt_id in history:
                print(f"✅ 生成完成！")
                return history[prompt_id]
            
            time.sleep(2)
            elapsed = int(time.time() - start_time)
            if elapsed % 10 == 0 and elapsed > 0:
                print(f"  ⏱️  已等待 {elapsed}秒...")
        
        print(f"❌ 等待超时（{timeout}秒）")
        return None
    
    def discover_workflows(self) -> Dict[str, List[str]]:
        """自动发现工作流类型"""
        object_info = self.get_object_info()
        
        workflows = {
            "text2image": [],
            "image2image": [],
            "text2video": [],
            "image2video": [],
            "inpaint": [],
            "controlnet": [],
        }
        
        # 分析节点，推断支持的工作流
        for node_name, node_info in object_info.items():
            # 文生图
            if any(k in node_name for k in ["KSampler", "CheckpointLoader", "CLIPTextEncode"]):
                workflows["text2image"].append(node_name)
            
            # 图生图
            if any(k in node_name for k in ["LoadImage", "VAEEncode"]):
                workflows["image2image"].append(node_name)
            
            # 文生视频
            if any(k in node_name for k in ["Video", "LTXV", "CogVideo", "Hunyuan"]):
                workflows["text2video"].append(node_name)
            
            # 图生视频
            if any(k in node_name for k in ["ImageToVideo", "I2V"]):
                workflows["image2video"].append(node_name)
            
            # Inpaint
            if "Inpaint" in node_name:
                workflows["inpaint"].append(node_name)
            
            # ControlNet
            if "ControlNet" in node_name:
                workflows["controlnet"].append(node_name)
        
        self.workflows = workflows
        return workflows
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """获取可用模型列表"""
        object_info = self.get_object_info()
        
        models = {
            "checkpoints": [],
            "lora": [],
            "vae": [],
            "clip": [],
            "controlnet": [],
        }
        
        # 从节点信息中提取模型信息
        for node_name, node_info in object_info.items():
            if "input" in node_info and "required" in node_info["input"]:
                inputs = node_info["input"]["required"]
                
                # 检查是否有模型选择输入
                if "ckpt_name" in inputs:
                    ckpt_input = inputs["ckpt_name"]
                    if isinstance(ckpt_input[0], list):
                        models["checkpoints"].extend(ckpt_input[0])
                
                if "lora_name" in inputs:
                    lora_input = inputs["lora_name"]
                    if isinstance(lora_input[0], list):
                        models["lora"].extend(lora_input[0])
                
                if "vae_name" in inputs:
                    vae_input = inputs["vae_name"]
                    if isinstance(vae_input[0], list):
                        models["vae"].extend(vae_input[0])
        
        # 去重
        for key in models:
            models[key] = list(set(models[key]))
        
        return models
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            queue = self.get_queue()
            print(f"✅ 连接成功！")
            print(f"  地址：{self.base_url}")
            print(f"  队列：{len(queue.get('queue_running', []))} 运行中")
            return True
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            return False


class ModelSearcher:
    """模型搜索器 - 搜索最佳实践"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; MarkHub/5.0)"
        })
    
    def search_huggingface(self, model_name: str) -> Dict:
        """搜索 HuggingFace 模型信息"""
        try:
            print(f"🔍 搜索 HuggingFace: {model_name}")
            
            # HuggingFace API
            api_url = f"https://huggingface.co/api/models/{model_name}"
            resp = self.session.get(api_url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "name": data.get("modelId", model_name),
                    "downloads": data.get("downloads", 0),
                    "likes": data.get("likes", 0),
                    "tags": data.get("tags", []),
                    "pipeline_tag": data.get("pipeline_tag", ""),
                    "description": data.get("cardData", {}).get("description", ""),
                }
            
            return {}
        except Exception as e:
            print(f"HuggingFace 搜索失败：{e}")
            return {}
    
    def search_github(self, repo_name: str) -> Dict:
        """搜索 GitHub 仓库信息"""
        try:
            print(f"🔍 搜索 GitHub: {repo_name}")
            
            api_url = f"https://api.github.com/repos/{repo_name}"
            resp = self.session.get(api_url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "name": data.get("full_name", repo_name),
                    "stars": data.get("stargazers_count", 0),
                    "description": data.get("description", ""),
                    "homepage": data.get("homepage", ""),
                    "topics": data.get("topics", []),
                }
            
            return {}
        except Exception as e:
            print(f"GitHub 搜索失败：{e}")
            return {}
    
    def get_best_practices(self, model_name: str, task_type: str) -> Dict:
        """获取最佳实践参数"""
        print(f"📊 获取最佳实践：{model_name} ({task_type})")
        
        # 基于模型类型的推荐参数
        recommendations = {
            "SDXL": {
                "width": 1024,
                "height": 1024,
                "steps": 30,
                "cfg": 7.0,
                "sampler": "DPM++ 2M Karras",
            },
            "Flux": {
                "width": 1024,
                "height": 1024,
                "steps": 25,
                "cfg": 3.5,
                "sampler": "Euler",
            },
            "LTX-Video": {
                "width": 1024,
                "height": 512,
                "frames": 241,
                "fps": 24,
                "steps": 25,
                "cfg": 3.0,
            },
            "CogVideoX": {
                "width": 720,
                "height": 480,
                "frames": 49,
                "fps": 8,
                "steps": 50,
                "cfg": 6.0,
            },
        }
        
        # 模糊匹配
        for key, params in recommendations.items():
            if key.lower() in model_name.lower():
                print(f"✅ 匹配到推荐参数：{key}")
                return params
        
        # 默认参数
        print("⚠️ 使用默认参数")
        return {
            "width": 512,
            "height": 512,
            "steps": 20,
            "cfg": 7.0,
        }


class WorkflowOptimizer:
    """工作流优化器"""
    
    def __init__(self, comfyui: ComfyUIRemote):
        self.comfyui = comfyui
        self.model_searcher = ModelSearcher()
    
    def optimize_text2image(self, prompt: str, model: str = "") -> Dict:
        """优化文生图工作流"""
        print(f"🎨 优化文生图工作流...")
        
        # 获取推荐参数
        params = self.model_searcher.get_best_practices(model or "SDXL", "text2image")
        
        # 创建工作流
        workflow = {
            "1": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": model or "v1-5-pruned-emaonly.ckpt"
                }
            },
            "2": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": prompt,
                    "clip": ["1", 1]
                }
            },
            "3": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": "ugly, deformed, low quality",
                    "clip": ["1", 1]
                }
            },
            "4": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "width": params.get("width", 512),
                    "height": params.get("height", 512),
                    "batch_size": 1
                }
            },
            "5": {
                "class_type": "KSampler",
                "inputs": {
                    "model": ["1", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["4", 0],
                    "seed": int(time.time() * 1000) % (2**31),
                    "steps": params.get("steps", 20),
                    "cfg": params.get("cfg", 7.0),
                    "sampler_name": params.get("sampler", "euler"),
                    "scheduler": "normal",
                    "denoise": 1.0
                }
            },
            "6": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2]
                }
            },
            "7": {
                "class_type": "SaveImage",
                "inputs": {
                    "images": ["6", 0],
                    "filename_prefix": "MarkHub",
                    "output_path": "output"
                }
            }
        }
        
        return workflow
    
    def optimize_text2video(self, prompt: str, model: str = "") -> Dict:
        """优化文生视频工作流"""
        print(f"🎬 优化文生视频工作流...")
        
        # 获取推荐参数
        params = self.model_searcher.get_best_practices(model or "LTX-Video", "text2video")
        
        # 检测远程服务器支持的节点
        object_info = self.comfyui.get_object_info()
        
        # 根据可用节点创建工作流
        if "EmptyLTXVLatentVideo" in object_info:
            # LTX-Video 工作流
            workflow = {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": model or "ltxv-13b-0.9.8-distilled.safetensors"}
                },
                "2": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": prompt, "clip": ["1", 1]}
                },
                "3": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": "", "clip": ["1", 1]}
                },
                "4": {
                    "class_type": "EmptyLTXVLatentVideo",
                    "inputs": {
                        "width": params.get("width", 1024),
                        "height": params.get("height", 512),
                        "length": params.get("frames", 241),
                        "batch_size": 1
                    }
                },
                "5": {
                    "class_type": "LTXVConditioning",
                    "inputs": {
                        "positive": ["2", 0],
                        "negative": ["3", 0],
                        "frame_rate": params.get("fps", 24)
                    }
                },
                "6": {
                    "class_type": "LTXVScheduler",
                    "inputs": {
                        "steps": params.get("steps", 25),
                        "cfg": params.get("cfg", 3.0),
                        "scheduler": "ltxv",
                        "shift": 1.0,
                        "use_dynamic_shift": True,
                        "seed": int(time.time() * 1000) % (2**31)
                    }
                },
                "7": {
                    "class_type": "LTXVBaseSampler",
                    "inputs": {
                        "model": ["1", 0],
                        "positive": ["5", 0],
                        "negative": ["3", 0],
                        "latent_image": ["4", 0],
                        "scheduler": ["6", 0],
                        "steps": params.get("steps", 25),
                        "cfg": params.get("cfg", 3.0),
                        "seed": int(time.time() * 1000) % (2**31)
                    }
                },
                "8": {
                    "class_type": "VAEDecode",
                    "inputs": {
                        "samples": ["7", 0],
                        "vae": ["1", 2]
                    }
                },
                "9": {
                    "class_type": "SaveVideo",
                    "inputs": {
                        "images": ["8", 0],
                        "frame_rate": params.get("fps", 24),
                        "output_path": "output",
                        "filename": "MarkHub_Video",
                        "format": "mp4",
                        "quality": 85
                    }
                }
            }
        else:
            # 通用视频工作流
            workflow = self._create_generic_video_workflow(prompt, params)
        
        return workflow
    
    def _create_generic_video_workflow(self, prompt: str, params: Dict) -> Dict:
        """创建通用视频工作流"""
        return {
            "1": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": "svd_xt.safetensors"}
            },
            "2": {
                "class_type": "ImageToVideo",
                "inputs": {
                    "positive": prompt,
                    "negative": "",
                    "width": params.get("width", 1024),
                    "height": params.get("height", 576),
                    "video_frames": params.get("frames", 25),
                    "motion_bucket_id": 127,
                    "fps": params.get("fps", 6),
                    "augmentation_level": 0.0,
                    "clip_vision": ["1", 1],
                    "vae": ["1", 2],
                    "model": ["1", 0]
                }
            },
            "3": {
                "class_type": "SaveVideo",
                "inputs": {
                    "images": ["2", 0],
                    "frame_rate": params.get("fps", 6),
                    "output_path": "output",
                    "filename": "MarkHub_Video"
                }
            }
        }


class MarkHubV5:
    """MarkHub v5.0 主类"""
    
    def __init__(self, comfyui_url: str):
        self.comfyui = ComfyUIRemote(comfyui_url)
        self.optimizer = WorkflowOptimizer(self.comfyui)
        self.output_dir = Path.home() / "Videos/MarkHub"
    
    def connect(self) -> bool:
        """连接到 ComfyUI"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                                                          ║")
        print("║     🚀 MarkHub v5.0 - 智能 ComfyUI 远程控制系统             ║")
        print("║                                                          ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        
        if not self.comfyui.test_connection():
            return False
        
        # 发现工作流
        workflows = self.comfyui.discover_workflows()
        print(f"📋 发现的工作流类型：")
        for wf_type, nodes in workflows.items():
            if nodes:
                print(f"  ✅ {wf_type}: {len(nodes)} 个节点")
        print()
        
        # 获取模型列表
        models = self.comfyui.get_available_models()
        if models["checkpoints"]:
            print(f"📦 可用模型：{len(models['checkpoints'])} 个")
        print()
        
        return True
    
    def generate_image(self, prompt: str, model: str = "", negative_prompt: str = "") -> bool:
        """生成图片"""
        print(f"🎨 生成图片...")
        print(f"  提示词：{prompt[:80]}...")
        print(f"  模型：{model or '自动选择'}")
        print()
        
        # 优化工作流
        workflow = self.optimizer.optimize_text2image(prompt, model)
        
        # 提交
        result = self.comfyui.queue_prompt(workflow)
        if not result:
            return False
        
        prompt_id = result.get('prompt_id')
        print(f"✅ 提交成功：{prompt_id}")
        
        # 等待完成
        history = self.comfyui.wait_for_prompt(prompt_id, timeout=300)
        if not history:
            return False
        
        # 下载结果
        outputs = history.get('outputs', {})
        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                for img in node_output['images']:
                    filename = img.get('filename')
                    if filename:
                        path = self.comfyui.download_file(filename, str(self.output_dir))
                        if path:
                            print(f"✅ 图片已保存：{path}")
                            return True
        
        return False
    
    def generate_video(self, prompt: str, model: str = "", duration: int = 10) -> bool:
        """生成视频"""
        print(f"🎬 生成视频...")
        print(f"  提示词：{prompt[:80]}...")
        print(f"  模型：{model or '自动选择'}")
        print(f"  时长：{duration}秒")
        print()
        
        # 优化工作流
        workflow = self.optimizer.optimize_text2video(prompt, model)
        
        # 提交
        result = self.comfyui.queue_prompt(workflow)
        if not result:
            return False
        
        prompt_id = result.get('prompt_id')
        print(f"✅ 提交成功：{prompt_id}")
        
        # 等待完成（视频需要更长时间）
        timeout = max(600, duration * 60)  # 至少 10 分钟
        history = self.comfyui.wait_for_prompt(prompt_id, timeout=timeout)
        if not history:
            return False
        
        # 下载结果
        outputs = history.get('outputs', {})
        for node_id, node_output in outputs.items():
            if 'videos' in node_output or 'gifs' in node_output:
                videos = node_output.get('videos', []) or node_output.get('gifs', [])
                for video in videos:
                    filename = video.get('filename')
                    if filename:
                        path = self.comfyui.download_file(filename, str(self.output_dir))
                        if path:
                            print(f"✅ 视频已保存：{path}")
                            return True
        
        return False
    
    def auto_generate(self, prompt: str, auto_detect: bool = True) -> bool:
        """自动生成（智能选择图片或视频）"""
        print(f"🤖 自动生成模式...")
        
        # 智能检测用户意图
        video_keywords = ["video", "motion", "animate", "动画", "视频", "跳舞", "走路"]
        is_video = any(kw in prompt.lower() for kw in video_keywords)
        
        if is_video:
            print("📹 检测到视频需求")
            return self.generate_video(prompt)
        else:
            print("🖼️ 检测到图片需求")
            return self.generate_image(prompt)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MarkHub v5.0 - 智能 ComfyUI 远程控制")
    parser.add_argument("--url", type=str, default="https://wp08.unicorn.org.cn:19329", help="ComfyUI 地址")
    parser.add_argument("-p", "--prompt", type=str, required=True, help="提示词")
    parser.add_argument("-m", "--model", type=str, default="", help="模型名称")
    parser.add_argument("-n", "--negative", type=str, default="", help="负面提示词")
    parser.add_argument("--video", action="store_true", help="生成视频")
    parser.add_argument("--image", action="store_true", help="生成图片")
    parser.add_argument("--auto", action="store_true", help="自动模式")
    parser.add_argument("--duration", type=int, default=10, help="视频时长（秒）")
    
    args = parser.parse_args()
    
    # 初始化
    markhub = MarkHubV5(args.url)
    
    if not markhub.connect():
        return 1
    
    # 生成
    if args.auto:
        success = markhub.auto_generate(args.prompt)
    elif args.video:
        success = markhub.generate_video(args.prompt, args.model, args.duration)
    else:
        success = markhub.generate_image(args.prompt, args.model, args.negative)
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
