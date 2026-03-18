#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkHub 独立版测试脚本
测试所有核心功能
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from markhub_standalone import MarkHub, Config, Logger

def test_init():
    """测试初始化"""
    print("\n" + "="*70)
    print("测试 1: 初始化")
    print("="*70)
    
    hub = MarkHub()
    print("✅ MarkHub 初始化成功")
    
    return hub

def test_check_models(hub):
    """测试模型检查"""
    print("\n" + "="*70)
    print("测试 2: 检查模型")
    print("="*70)
    
    all_exist = hub._check_models()
    
    if all_exist:
        print("✅ 所有模型已存在")
    else:
        print("⚠️ 部分模型缺失，运行以下命令下载:")
        print("   python3 markhub_standalone.py --download-models")
    
    return all_exist

def test_sd_cpp(hub):
    """测试 stable-diffusion.cpp"""
    print("\n" + "="*70)
    print("测试 3: 检查 stable-diffusion.cpp")
    print("="*70)
    
    installed = hub.installer.check_sd_cpp()
    
    if installed:
        print("✅ stable-diffusion.cpp 已安装")
        print(f"   路径：{Config.SD_CPP_BIN}")
    else:
        print("⚠️ stable-diffusion.cpp 未安装")
        print("   运行以下命令安装:")
        print("   python3 markhub_standalone.py --install-sd-cpp")
    
    return installed

def test_error_solver(hub):
    """测试错误解决器"""
    print("\n" + "="*70)
    print("测试 4: 错误解决器")
    print("="*70)
    
    test_errors = [
        "model file not found: z_image_turbo-Q8_0.gguf",
        "CUDA out of memory: tried to allocate 2.5GB",
        "Permission denied: /path/to/model",
        "stable-diffusion.cpp failed to load"
    ]
    
    for error in test_errors:
        print(f"\n测试错误：{error}")
        solutions = hub.solver.solve(error)
        
        if solutions:
            for sol in solutions:
                print(f"  来源：{sol['source']}")
                for item in sol['results'][:2]:
                    if 'title' in item:
                        print(f"    - {item['title']}")
        else:
            print("  无解决方案")
    
    print("✅ 错误解决器测试完成")

def test_dependencies(hub):
    """测试依赖检查"""
    print("\n" + "="*70)
    print("测试 5: 检查 Python 依赖")
    print("="*70)
    
    result = hub.installer.check_dependencies()
    
    if result:
        print("✅ 所有依赖已安装")
    
    return result

def test_config():
    """测试配置"""
    print("\n" + "="*70)
    print("测试 6: 检查配置")
    print("="*70)
    
    print(f"基础目录：{Config.BASE_DIR}")
    print(f"模型目录：{Config.MODELS_DIR}")
    print(f"输出目录：{Config.OUTPUT_DIR}")
    print(f"默认分辨率：{Config.DEFAULT_WIDTH}x{Config.DEFAULT_HEIGHT}")
    print(f"默认步数：{Config.DEFAULT_STEPS}")
    print(f"默认 CFG: {Config.DEFAULT_CFG}")
    
    # 检查目录是否存在
    for dir_path, name in [
        (Config.BASE_DIR, "基础目录"),
        (Config.MODELS_DIR, "模型目录"),
        (Config.OUTPUT_DIR, "输出目录"),
        (Config.LOG_DIR, "日志目录")
    ]:
        if dir_path.exists():
            print(f"✅ {name} 存在：{dir_path}")
        else:
            print(f"❌ {name} 不存在：{dir_path}")
    
    print("✅ 配置测试完成")

def main():
    """运行所有测试"""
    print("\n" + "="*70)
    print("🧪 MarkHub 独立版测试套件")
    print("="*70)
    
    results = {}
    
    try:
        # 测试 1: 配置
        test_config()
        results["配置"] = "✅"
        
        # 测试 2: 初始化
        hub = test_init()
        results["初始化"] = "✅"
        
        # 测试 3: 依赖
        result = test_dependencies(hub)
        results["依赖检查"] = "✅" if result else "⚠️"
        
        # 测试 4: 模型
        result = test_check_models(hub)
        results["模型检查"] = "✅" if result else "⚠️"
        
        # 测试 5: stable-diffusion.cpp
        result = test_sd_cpp(hub)
        results["sd.cpp 检查"] = "✅" if result else "⚠️"
        
        # 测试 6: 错误解决器
        test_error_solver(hub)
        results["错误解决器"] = "✅"
        
    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        results["异常"] = "❌"
    
    # 打印总结
    print("\n" + "="*70)
    print("📊 测试总结")
    print("="*70)
    
    for test_name, result in results.items():
        print(f"  {test_name}: {result}")
    
    print("\n" + "="*70)
    
    # 检查是否全部通过
    if all(r == "✅" for r in results.values()):
        print("🎉 所有测试通过！")
        print("\n下一步:")
        print("  1. 如果模型未下载：python3 markhub_standalone.py --download-models")
        print("  2. 如果 sd.cpp 未安装：python3 markhub_standalone.py --install-sd-cpp")
        print("  3. 生成图片：python3 markhub_standalone.py -p 'your prompt'")
    else:
        print("⚠️ 部分测试未通过，请查看上方详情")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
