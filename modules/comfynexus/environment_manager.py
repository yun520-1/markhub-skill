#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyNexus 环境管理模块
提供 Python/PyTorch 版本检测、环境快照、端口冲突检测等功能
"""

import sys
import os
import json
import subprocess
import socket
import shutil
from datetime import datetime
from pathlib import Path

class EnvironmentManager:
    """环境管理器 - 借鉴 ComfyNexus 的环境管理功能"""
    
    def __init__(self, comfyui_dir=None):
        self.comfyui_dir = Path(comfyui_dir) if comfyui_dir else None
        self.snapshots_dir = Path("~/ComfyNexus/snapshots").expanduser()
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
    
    def detect_python_version(self):
        """检测 Python 版本"""
        version = sys.version_info
        return {
            "version": f"{version.major}.{version.minor}.{version.micro}",
            "major": version.major,
            "minor": version.minor,
            "micro": version.micro,
            "executable": sys.executable
        }
    
    def detect_pytorch_version(self):
        """检测 PyTorch 版本"""
        try:
            import torch
            return {
                "version": torch.__version__,
                "cuda_available": torch.cuda.is_available(),
                "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
                "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
            }
        except ImportError:
            return {"version": "Not installed", "error": "PyTorch not found"}
    
    def detect_comfyui_version(self):
        """检测 ComfyUI 版本"""
        if not self.comfyui_dir:
            return {"error": "ComfyUI directory not set"}
        
        version_file = self.comfyui_dir / "pyproject.toml"
        if version_file.exists():
            try:
                with open(version_file, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if 'version' in line and '=' in line:
                            version = line.split('=')[1].strip().strip('"\'')
                            return {"version": version}
            except:
                pass
        
        # 尝试 git 检测
        git_dir = self.comfyui_dir / ".git"
        if git_dir.exists():
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    cwd=self.comfyui_dir,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return {"version": f"git-{result.stdout.strip()}"}
            except:
                pass
        
        return {"version": "Unknown"}
    
    def check_port_conflict(self, port):
        """检查端口冲突"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            return {
                "port": port,
                "in_use": result == 0,
                "status": "占用" if result == 0 else "可用"
            }
        finally:
            sock.close()
    
    def detect_comfyui_instances(self):
        """检测运行中的 ComfyUI 实例"""
        common_ports = [8188, 8189, 8080, 3000, 4000, 40000, 40001]
        instances = []
        
        for port in common_ports:
            status = self.check_port_conflict(port)
            if status["in_use"]:
                instances.append({
                    "port": port,
                    "url": f"http://localhost:{port}",
                    "status": "running"
                })
        
        return instances
    
    def create_snapshot(self, name=None):
        """创建环境快照"""
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"snapshot_{timestamp}"
        
        snapshot = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "python": self.detect_python_version(),
            "pytorch": self.detect_pytorch_version(),
            "comfyui": self.detect_comfyui_version() if self.comfyui_dir else None,
            "instances": self.detect_comfyui_instances()
        }
        
        # 如果设置了 ComfyUI 目录，保存插件列表
        if self.comfyui_dir:
            custom_nodes = self.comfyui_dir / "custom_nodes"
            if custom_nodes.exists():
                plugins = [d.name for d in custom_nodes.iterdir() if d.is_dir()]
                snapshot["plugins"] = plugins
        
        # 保存快照
        snapshot_file = self.snapshots_dir / f"{name}.json"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "name": name,
            "file": str(snapshot_file)
        }
    
    def list_snapshots(self):
        """列出所有快照"""
        snapshots = []
        for file in self.snapshots_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    snapshots.append({
                        "name": data.get("name", file.stem),
                        "created_at": data.get("created_at", "Unknown"),
                        "file": str(file)
                    })
            except:
                pass
        
        return sorted(snapshots, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def restore_snapshot(self, name):
        """恢复快照 (仅显示信息，不实际修改环境)"""
        snapshot_file = self.snapshots_dir / f"{name}.json"
        
        if not snapshot_file.exists():
            return {"success": False, "error": f"Snapshot '{name}' not found"}
        
        with open(snapshot_file, 'r', encoding='utf-8') as f:
            snapshot = json.load(f)
        
        return {
            "success": True,
            "snapshot": snapshot,
            "message": f"快照 '{name}' 信息已读取。注意：实际恢复需要手动操作。"
        }
    
    def get_system_info(self):
        """获取系统信息"""
        import platform
        
        # 内存信息
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_info = {
                "total": f"{memory.total / 1024**3:.1f} GB",
                "available": f"{memory.available / 1024**3:.1f} GB",
                "percent": memory.percent
            }
        except:
            memory_info = {"error": "psutil not installed"}
        
        # 磁盘信息
        try:
            disk = shutil.disk_usage("/")
            disk_info = {
                "total": f"{disk.total / 1024**3:.1f} GB",
                "used": f"{disk.used / 1024**3:.1f} GB",
                "free": f"{disk.free / 1024**3:.1f} GB",
                "percent": disk.percent
            }
        except:
            disk_info = {"error": "Could not get disk info"}
        
        return {
            "os": f"{platform.system()} {platform.release()}",
            "python": self.detect_python_version(),
            "pytorch": self.detect_pytorch_version(),
            "memory": memory_info,
            "disk": disk_info,
            "comfyui_instances": self.detect_comfyui_instances()
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ComfyNexus 环境管理工具')
    parser.add_argument('--action', '-a', choices=[
        'info', 'snapshot', 'list-snapshots', 'restore', 'check-port', 'detect-instances'
    ], default='info', help='操作类型')
    parser.add_argument('--name', '-n', help='快照名称')
    parser.add_argument('--port', '-p', type=int, help='检查的端口号')
    parser.add_argument('--comfyui-dir', '-c', help='ComfyUI 目录')
    
    args = parser.parse_args()
    
    manager = EnvironmentManager(comfyui_dir=args.comfyui_dir)
    
    if args.action == 'info':
        info = manager.get_system_info()
        print("=" * 60)
        print("  ComfyNexus 环境信息")
        print("=" * 60)
        print(f"\n🖥️  操作系统：{info['os']}")
        print(f"\n🐍 Python: {info['python']['version']}")
        print(f"   路径：{info['python']['executable']}")
        print(f"\n🔦 PyTorch: {info['pytorch']['version']}")
        if 'cuda_available' in info['pytorch']:
            print(f"   CUDA: {'✅ ' if info['pytorch']['cuda_available'] else '❌ '} {info['pytorch'].get('cuda_version', 'N/A')}")
        print(f"\n💾 内存：{info['memory'].get('total', 'N/A')} (可用：{info['memory'].get('available', 'N/A')})")
        print(f"\n📁 磁盘：{info['disk'].get('total', 'N/A')} (已用：{info['disk'].get('used', 'N/A')})")
        
        instances = info.get('comfyui_instances', [])
        if instances:
            print(f"\n🚀 运行中的 ComfyUI 实例:")
            for inst in instances:
                print(f"   - 端口 {inst['port']}: {inst['url']}")
        else:
            print(f"\n🚀 运行中的 ComfyUI 实例：无")
        
    elif args.action == 'snapshot':
        result = manager.create_snapshot(args.name)
        if result['success']:
            print(f"✅ 快照创建成功：{result['name']}")
            print(f"📁 保存位置：{result['file']}")
        else:
            print(f"❌ 快照创建失败：{result.get('error', 'Unknown')}")
    
    elif args.action == 'list-snapshots':
        snapshots = manager.list_snapshots()
        if snapshots:
            print(f"📋 环境快照列表:")
            for i, snap in enumerate(snapshots, 1):
                print(f"  {i}. {snap['name']} ({snap['created_at']})")
        else:
            print("📋 没有找到快照")
    
    elif args.action == 'restore':
        if not args.name:
            print("❌ 请指定快照名称 (--name)")
            return
        result = manager.restore_snapshot(args.name)
        if result['success']:
            print(f"✅ 快照 '{args.name}' 信息:")
            snapshot = result['snapshot']
            print(f"   创建时间：{snapshot.get('created_at', 'Unknown')}")
            print(f"   Python: {snapshot.get('python', {}).get('version', 'N/A')}")
            print(f"   PyTorch: {snapshot.get('pytorch', {}).get('version', 'N/A')}")
        else:
            print(f"❌ 错误：{result.get('error', 'Unknown')}")
    
    elif args.action == 'check-port':
        if not args.port:
            print("❌ 请指定端口号 (--port)")
            return
        result = manager.check_port_conflict(args.port)
        status = "✅ 可用" if not result['in_use'] else "❌ 已占用"
        print(f"端口 {args.port}: {status}")
    
    elif args.action == 'detect-instances':
        instances = manager.detect_comfyui_instances()
        if instances:
            print(f"🚀 发现 {len(instances)} 个运行中的 ComfyUI 实例:")
            for inst in instances:
                print(f"   - {inst['url']}")
        else:
            print("🚀 未发现运行中的 ComfyUI 实例")


if __name__ == "__main__":
    main()
