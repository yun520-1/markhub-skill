#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyNexus 插件管理模块
提供插件列表、安装、更新、冲突检测等功能
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime

class PluginManager:
    """插件管理器 - 借鉴 ComfyNexus 的插件管理功能"""
    
    def __init__(self, comfyui_dir=None):
        self.comfyui_dir = Path(comfyui_dir) if comfyui_dir else None
        self.custom_nodes_dir = None
        if self.comfyui_dir:
            self.custom_nodes_dir = self.comfyui_dir / "custom_nodes"
        
        # GitHub API 配置
        self.github_token = os.environ.get("GITHUB_TOKEN", None)
        self.api_base = "https://api.github.com"
    
    def set_github_token(self, token):
        """设置 GitHub Token (提升 API 限制)"""
        self.github_token = token
    
    def list_plugins(self):
        """列出已安装的插件"""
        if not self.custom_nodes_dir or not self.custom_nodes_dir.exists():
            return {"error": "Custom nodes directory not found"}
        
        plugins = []
        for plugin_dir in self.custom_nodes_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith('.'):
                plugin_info = {
                    "name": plugin_dir.name,
                    "path": str(plugin_dir),
                    "installed": True
                }
                
                # 尝试读取 package.json 或 pyproject.toml
                package_json = plugin_dir / "package.json"
                if package_json.exists():
                    try:
                        with open(package_json, 'r') as f:
                            pkg = json.load(f)
                            plugin_info["version"] = pkg.get("version", "Unknown")
                            plugin_info["description"] = pkg.get("description", "")
                            plugin_info["author"] = pkg.get("author", "")
                    except:
                        pass
                
                # 尝试读取 git remote
                git_dir = plugin_dir / ".git"
                if git_dir.exists():
                    try:
                        result = subprocess.run(
                            ["git", "config", "--get", "remote.origin.url"],
                            cwd=plugin_dir,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode == 0:
                            plugin_info["repository"] = result.stdout.strip()
                    except:
                        pass
                
                plugins.append(plugin_info)
        
        return {
            "count": len(plugins),
            "plugins": sorted(plugins, key=lambda x: x["name"])
        }
    
    def get_plugin_info(self, plugin_name):
        """获取插件详细信息"""
        if not self.custom_nodes_dir:
            return {"error": "Custom nodes directory not set"}
        
        plugin_dir = self.custom_nodes_dir / plugin_name
        if not plugin_dir.exists():
            return {"error": f"Plugin '{plugin_name}' not found"}
        
        return self._scan_plugin(plugin_dir)
    
    def _scan_plugin(self, plugin_dir):
        """扫描插件信息"""
        info = {
            "name": plugin_dir.name,
            "path": str(plugin_dir)
        }
        
        # 读取 README
        readme_files = ["README.md", "readme.md", "README.txt"]
        for readme in readme_files:
            readme_path = plugin_dir / readme
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        info["readme"] = f.read()[:1000]  # 前 1000 字符
                    break
                except:
                    pass
        
        # 读取 requirements.txt
        req_file = plugin_dir / "requirements.txt"
        if req_file.exists():
            try:
                with open(req_file, 'r') as f:
                    info["requirements"] = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except:
                pass
        
        return info
    
    def check_updates(self):
        """检查插件更新"""
        if not self.custom_nodes_dir or not self.custom_nodes_dir.exists():
            return {"error": "Custom nodes directory not found"}
        
        updates = []
        for plugin_dir in self.custom_nodes_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith('.'):
                git_dir = plugin_dir / ".git"
                if git_dir.exists():
                    try:
                        # 获取当前分支
                        branch_result = subprocess.run(
                            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            cwd=plugin_dir,
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        if branch_result.returncode != 0:
                            continue
                        
                        branch = branch_result.stdout.strip()
                        
                        # 获取远程最新 commit
                        fetch_result = subprocess.run(
                            ["git", "fetch", "origin", branch],
                            cwd=plugin_dir,
                            capture_output=True,
                            timeout=10
                        )
                        
                        # 比较本地和远程
                        local_result = subprocess.run(
                            ["git", "rev-parse", "HEAD"],
                            cwd=plugin_dir,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        remote_result = subprocess.run(
                            ["git", "rev-parse", f"origin/{branch}"],
                            cwd=plugin_dir,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        if local_result.returncode == 0 and remote_result.returncode == 0:
                            local_commit = local_result.stdout.strip()
                            remote_commit = remote_result.stdout.strip()
                            
                            if local_commit != remote_commit:
                                updates.append({
                                    "name": plugin_dir.name,
                                    "current": local_commit[:7],
                                    "available": remote_commit[:7],
                                    "status": "update_available"
                                })
                    except Exception as e:
                        pass
        
        return {
            "total": len(updates),
            "updates": updates
        }
    
    def update_plugin(self, plugin_name):
        """更新单个插件"""
        if not self.custom_nodes_dir:
            return {"error": "Custom nodes directory not set"}
        
        plugin_dir = self.custom_nodes_dir / plugin_name
        if not plugin_dir.exists():
            return {"error": f"Plugin '{plugin_name}' not found"}
        
        git_dir = plugin_dir / ".git"
        if not git_dir.exists():
            return {"error": "Not a git repository"}
        
        try:
            # 拉取更新
            result = subprocess.run(
                ["git", "pull"],
                cwd=plugin_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {"error": "Update timeout"}
        except Exception as e:
            return {"error": str(e)}
    
    def update_all(self):
        """更新所有插件"""
        updates = self.check_updates()
        results = []
        
        for plugin in updates.get("updates", []):
            result = self.update_plugin(plugin["name"])
            results.append({
                "name": plugin["name"],
                "success": result.get("success", False),
                "message": result.get("output", result.get("error", "Unknown"))
            })
        
        return {
            "total": len(results),
            "updated": sum(1 for r in results if r["success"]),
            "results": results
        }
    
    def check_conflicts(self):
        """检测插件冲突"""
        if not self.custom_nodes_dir or not self.custom_nodes_dir.exists():
            return {"error": "Custom nodes directory not found"}
        
        conflicts = []
        
        # 检查节点名称冲突
        node_names = {}
        for plugin_dir in self.custom_nodes_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith('.'):
                # 扫描 Python 文件中的 NODE_CLASS_MAPPINGS
                for py_file in plugin_dir.glob("*.py"):
                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if 'NODE_CLASS_MAPPINGS' in content:
                                # 简单解析 (实际应该用 AST)
                                for line in content.split('\n'):
                                    if '=' in line and 'NODE_CLASS_MAPPINGS' not in line:
                                        name = line.split('=')[0].strip().strip('"\'')
                                        if name and not name.startswith('#'):
                                            if name in node_names:
                                                conflicts.append({
                                                    "type": "node_name_conflict",
                                                    "node": name,
                                                    "plugins": [node_names[name], plugin_dir.name]
                                                })
                                            else:
                                                node_names[name] = plugin_dir.name
                    except:
                        pass
        
        return {
            "has_conflicts": len(conflicts) > 0,
            "count": len(conflicts),
            "conflicts": conflicts
        }
    
    def search_github(self, query, limit=10):
        """搜索 GitHub 上的 ComfyUI 插件"""
        headers = {}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        try:
            response = requests.get(
                f"{self.api_base}/search/repositories",
                headers=headers,
                params={
                    "q": f"comfyui {query} in:name,description",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": limit
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "count": data.get("total_count", 0),
                    "items": [
                        {
                            "name": item["name"],
                            "full_name": item["full_name"],
                            "description": item.get("description", ""),
                            "stars": item.get("stargazers_count", 0),
                            "url": item["html_url"],
                            "clone_url": item["clone_url"]
                        }
                        for item in data.get("items", [])
                    ]
                }
            else:
                return {"error": f"GitHub API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ComfyNexus 插件管理工具')
    parser.add_argument('--action', '-a', choices=[
        'list', 'info', 'check-updates', 'update', 'update-all', 'check-conflicts', 'search'
    ], default='list', help='操作类型')
    parser.add_argument('--plugin', '-p', help='插件名称')
    parser.add_argument('--query', '-q', help='搜索关键词')
    parser.add_argument('--comfyui-dir', '-c', help='ComfyUI 目录')
    parser.add_argument('--github-token', '-t', help='GitHub Token')
    
    args = parser.parse_args()
    
    manager = PluginManager(comfyui_dir=args.comfyui_dir)
    
    if args.github_token:
        manager.set_github_token(args.github_token)
    
    if args.action == 'list':
        result = manager.list_plugins()
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"📦 已安装插件：{result['count']} 个")
            print("-" * 60)
            for plugin in result['plugins'][:20]:  # 显示前 20 个
                print(f"  • {plugin['name']}")
                if 'version' in plugin:
                    print(f"    版本：{plugin['version']}")
                if 'description' in plugin:
                    print(f"    说明：{plugin['description'][:50]}...")
            if len(result['plugins']) > 20:
                print(f"  ... 还有 {len(result['plugins']) - 20} 个插件")
    
    elif args.action == 'info':
        if not args.plugin:
            print("❌ 请指定插件名称 (--plugin)")
            return
        result = manager.get_plugin_info(args.plugin)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"📦 插件信息：{result['name']}")
            print(f"   路径：{result['path']}")
            if 'version' in result:
                print(f"   版本：{result['version']}")
            if 'repository' in result:
                print(f"   仓库：{result['repository']}")
    
    elif args.action == 'check-updates':
        result = manager.check_updates()
        if "error" in result:
            print(f"❌ {result['error']}")
        elif result['total'] == 0:
            print("✅ 所有插件已是最新版本")
        else:
            print(f"🔄 发现 {result['total']} 个可更新插件:")
            for plugin in result['updates']:
                print(f"  • {plugin['name']}: {plugin['current']} → {plugin['available']}")
    
    elif args.action == 'update':
        if not args.plugin:
            print("❌ 请指定插件名称 (--plugin)")
            return
        print(f"🔄 更新 {args.plugin}...")
        result = manager.update_plugin(args.plugin)
        if result.get("success"):
            print(f"✅ 更新成功")
        else:
            print(f"❌ 更新失败：{result.get('error', 'Unknown')}")
    
    elif args.action == 'update-all':
        print("🔄 更新所有插件...")
        result = manager.update_all()
        print(f"✅ 完成：{result['updated']}/{result['total']} 个插件更新成功")
    
    elif args.action == 'check-conflicts':
        result = manager.check_conflicts()
        if "error" in result:
            print(f"❌ {result['error']}")
        elif result['has_conflicts']:
            print(f"⚠️  发现 {result['count']} 个冲突:")
            for conflict in result['conflicts'][:10]:
                print(f"  • {conflict['type']}: {conflict['node']} ({', '.join(conflict['plugins'])})")
        else:
            print("✅ 未发现插件冲突")
    
    elif args.action == 'search':
        if not args.query:
            print("❌ 请指定搜索关键词 (--query)")
            return
        print(f"🔍 搜索：{args.query}...")
        result = manager.search_github(args.query)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"📊 找到 {result['count']} 个结果:")
            for item in result['items'][:10]:
                print(f"\n  ⭐ {item['name']} ({item['stars']} ⭐)")
                print(f"     {item['description'][:60]}...")
                print(f"     {item['url']}")


if __name__ == "__main__":
    main()
