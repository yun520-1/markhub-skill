#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zopia AI 视频制作集成模块
通过 Zopia API 驱动 AI 视频制作全流程：创建项目、配置风格、与 Agent 对话生成剧本/角色/分镜/视频
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime

class ZopiaClient:
    """Zopia API 客户端 - AI 视频制作全流程"""
    
    def __init__(self, token=None, base_url="https://zopia.ai"):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        
        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
    
    def set_token(self, token):
        """设置 API Token"""
        self.token = token
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
    
    def create_project(self, name=None, lang="zh-CN"):
        """创建项目"""
        url = f"{self.base_url}/api/base/create"
        payload = {
            "baseName": name or f"MarkHub_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "lang": lang
        }
        
        response = self.session.post(url, json=payload)
        if response.status_code == 201:
            data = response.json()
            return {
                "success": True,
                "base_id": data["data"]["baseId"],
                "base_name": data["data"]["baseName"],
                "base_url": f"{self.base_url}/base/{data['data']['baseId']}"
            }
        else:
            return {"success": False, "error": response.text, "status_code": response.status_code}
    
    def save_settings(self, base_id, settings):
        """保存项目设置
        
        Args:
            base_id: 项目 ID
            settings: 设置字典，包含：
                - locale: 对白语言 (zh-CN, en, ja)
                - aspect_ratio: 画面比例 (16:9, 9:16)
                - style: 视觉风格 (anime_japanese_korean, realistic_3d_cg, etc.)
                - generation_method: 生成方法 (n_grid, multi_ref, start_frame)
                - video_model: 视频模型
                - image_size: 关键帧分辨率 (1K, 2K, 4K)
                - video_resolution: 视频分辨率 (480p, 720p, 1080p)
        """
        url = f"{self.base_url}/api/base/settings"
        payload = {
            "base_id": base_id,
            "settings": settings
        }
        
        response = self.session.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "settings": data.get("settings", {})}
        else:
            error_data = response.json() if response.text else {}
            return {
                "success": False,
                "error": error_data.get("error", "Unknown error"),
                "message": error_data.get("message", response.text),
                "status_code": response.status_code
            }
    
    def get_settings(self, base_id):
        """获取项目设置"""
        url = f"{self.base_url}/api/base/settings"
        params = {"base_id": base_id}
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "settings": data.get("settings", {})}
        else:
            return {"success": False, "error": response.text}
    
    def agent_chat(self, base_id, message, session_id=None):
        """与项目 Agent 对话
        
        Args:
            base_id: 项目 ID
            message: 自然语言指令
            session_id: 可选，用于多轮对话续接
        
        Returns:
            session_id: 会话 ID (首次调用会生成)
            reply: Agent 回复
            actions: 执行的动作列表
            workspace: 项目工作区状态
        """
        url = f"{self.base_url}/api/v1/agent/chat"
        payload = {
            "base_id": base_id,
            "message": message
        }
        
        if session_id:
            payload["session_id"] = session_id
        
        response = self.session.post(url, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "session_id": data.get("session_id"),
                "base_id": data.get("base_id"),
                "base_url": data.get("base_url"),
                "reply": data.get("reply", {}),
                "actions": data.get("actions", []),
                "workspace": data.get("workspace", {})
            }
        elif response.status_code == 409:
            return {
                "success": False,
                "error": "session_busy",
                "message": "正在执行中，请稍后再重新尝试"
            }
        else:
            error_data = response.json() if response.text else {}
            return {
                "success": False,
                "error": error_data.get("error", "Unknown error"),
                "message": error_data.get("message", response.text),
                "status_code": response.status_code
            }
    
    def list_projects(self):
        """获取项目列表"""
        url = f"{self.base_url}/api/base/list"
        
        response = self.session.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "projects": data.get("data", [])
            }
        else:
            return {"success": False, "error": response.text}
    
    def get_project(self, base_id):
        """获取项目详情"""
        url = f"{self.base_url}/api/base/{base_id}"
        
        response = self.session.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "name": data.get("name"),
                "sessions": data.get("sessions", []),
                "settings": data.get("settings", {}),
                "profile": data.get("profile", {})
            }
        else:
            return {"success": False, "error": response.text}
    
    def get_balance(self):
        """查询积分余额"""
        url = f"{self.base_url}/api/billing/getBalance"
        
        response = self.session.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "accounts": data.get("accounts", []),
                "summary": data.get("summary", {})
            }
        else:
            return {"success": False, "error": response.text}


# 预设配置
ZOpia_PRESETS = {
    "anime_standard": {
        "name": "日本动画标准",
        "settings": {
            "locale": "zh-CN",
            "aspect_ratio": "16:9",
            "style": "anime_japanese_korean",
            "generation_method": "n_grid",
            "video_model": "generate_video_by_kling_o3",
            "image_size": "2K",
            "video_resolution": "720p"
        }
    },
    "realistic_3d": {
        "name": "3D CG 写实",
        "settings": {
            "locale": "zh-CN",
            "aspect_ratio": "16:9",
            "style": "realistic_3d_cg",
            "generation_method": "n_grid",
            "video_model": "generate_video_by_kling_o3",
            "image_size": "2K",
            "video_resolution": "720p"
        }
    },
    "pixar_cartoon": {
        "name": "Pixar 卡通",
        "settings": {
            "locale": "zh-CN",
            "aspect_ratio": "16:9",
            "style": "pixar_3d_cartoon",
            "generation_method": "n_grid",
            "video_model": "generate_video_by_kling_o3",
            "image_size": "2K",
            "video_resolution": "720p"
        }
    },
    "vertical_short": {
        "name": "竖屏短视频",
        "settings": {
            "locale": "zh-CN",
            "aspect_ratio": "9:16",
            "style": "anime_japanese_korean",
            "generation_method": "n_grid",
            "video_model": "generate_video_by_kling_o3",
            "image_size": "2K",
            "video_resolution": "720p"
        }
    }
}


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Zopia AI 视频制作工具')
    parser.add_argument('--token', '-t', help='Zopia API Token')
    parser.add_argument('--action', '-a', choices=[
        'create', 'settings', 'chat', 'list', 'info', 'balance'
    ], default='list', help='操作类型')
    parser.add_argument('--base-id', '-b', help='项目 ID')
    parser.add_argument('--message', '-m', help='Agent 对话消息')
    parser.add_argument('--session-id', '-s', help='会话 ID (多轮对话)')
    parser.add_argument('--preset', '-p', choices=list(ZOpia_PRESETS.keys()), help='预设配置')
    parser.add_argument('--name', '-n', help='项目名称')
    
    args = parser.parse_args()
    
    if not args.token:
        print("❌ 请提供 Zopia API Token (--token)")
        print("\n📝 获取 Token 步骤:")
        print("   1. 访问 https://zopia.ai/settings/api-tokens")
        print("   2. 登录后点击'生成新 Token'")
        print("   3. 复制 Token 格式：zopia-xxxxxxxxxxxx")
        return
    
    client = ZopiaClient(token=args.token)
    
    if args.action == 'create':
        print("🎬 创建 Zopia 项目...")
        result = client.create_project(name=args.name)
        if result["success"]:
            print(f"✅ 项目创建成功!")
            print(f"   名称：{result['base_name']}")
            print(f"   ID: {result['base_id']}")
            print(f"   URL: {result['base_url']}")
        else:
            print(f"❌ 创建失败：{result.get('error', 'Unknown')}")
    
    elif args.action == 'settings':
        if not args.base_id:
            print("❌ 请提供项目 ID (--base-id)")
            return
        
        if args.preset:
            preset = ZOpia_PRESETS[args.preset]
            print(f"📋 应用预设：{preset['name']}")
            result = client.save_settings(args.base_id, preset["settings"])
        else:
            # 读取设置
            result = client.get_settings(args.base_id)
        
        if result["success"]:
            print("✅ 设置操作成功")
            if "settings" in result:
                print("\n当前设置:")
                for key, value in result["settings"].items():
                    print(f"   {key}: {value}")
        else:
            print(f"❌ 操作失败：{result.get('message', result.get('error', 'Unknown'))}")
    
    elif args.action == 'chat':
        if not args.base_id:
            print("❌ 请提供项目 ID (--base-id)")
            return
        if not args.message:
            print("❌ 请提供消息内容 (--message)")
            return
        
        print(f"🤖 与 Agent 对话...")
        result = client.agent_chat(args.base_id, args.message, args.session_id)
        
        if result["success"]:
            print(f"✅ Agent 回复:")
            if "reply" in result:
                reply = result["reply"]
                print(f"   Agent: {reply.get('agent', 'Unknown')}")
                print(f"   回复：{reply.get('text', '')[:500]}...")
            
            if result.get("session_id") and not args.session_id:
                print(f"\n💡 会话 ID: {result['session_id']}")
                print(f"   后续对话请添加 --session-id {result['session_id']}")
            
            if "actions" in result and result["actions"]:
                print(f"\n📊 执行动作:")
                for action in result["actions"]:
                    print(f"   • {action.get('tool_name', 'Unknown')}: {action.get('status', 'Unknown')}")
        else:
            print(f"❌ 对话失败：{result.get('message', result.get('error', 'Unknown'))}")
    
    elif args.action == 'list':
        print("📋 获取项目列表...")
        result = client.list_projects()
        
        if result["success"] and result["projects"]:
            print(f"\n找到 {len(result['projects'])} 个项目:\n")
            for i, proj in enumerate(result["projects"][:10], 1):
                print(f"{i}. {proj.get('name', 'Unnamed')}")
                print(f"   ID: {proj.get('id', 'Unknown')}")
                print(f"   创建：{proj.get('createdAt', 'Unknown')}")
                print(f"   更新：{proj.get('updatedAt', 'Unknown')}")
                if proj.get('thumbnails'):
                    print(f"   缩略图：{len(proj['thumbnails'])} 张")
                print()
        elif result["success"]:
            print("📋 暂无项目")
        else:
            print(f"❌ 获取失败：{result.get('error', 'Unknown')}")
    
    elif args.action == 'info':
        if not args.base_id:
            print("❌ 请提供项目 ID (--base-id)")
            return
        
        print(f"📊 获取项目详情...")
        result = client.get_project(args.base_id)
        
        if result["success"]:
            print(f"\n项目名称：{result['name']}")
            print(f"\n设置:")
            for key, value in result.get("settings", {}).items():
                print(f"   {key}: {value}")
            
            sessions = result.get("sessions", [])
            if sessions:
                print(f"\n会话 ({len(sessions)}个):")
                for sess in sessions[:5]:
                    print(f"   • {sess.get('title', 'Untitled')} ({sess.get('id', 'Unknown')})")
        else:
            print(f"❌ 获取失败：{result.get('error', 'Unknown')}")
    
    elif args.action == 'balance':
        print("💰 查询积分余额...")
        result = client.get_balance()
        
        if result["success"]:
            accounts = result.get("accounts", [])
            summary = result.get("summary", {})
            
            print(f"\n积分账户:")
            for acc in accounts:
                print(f"   • {acc.get('credit_type', 'Unknown')}: {acc.get('balance', '0')} (到期：{acc.get('expires_at', 'N/A')})")
            
            if summary:
                print(f"\n汇总:")
                print(f"   总余额：{summary.get('totalBalance', '0')}")
                print(f"   可用：{summary.get('totalAvailable', '0')}")
        else:
            print(f"❌ 查询失败：{result.get('error', 'Unknown')}")


if __name__ == "__main__":
    main()
