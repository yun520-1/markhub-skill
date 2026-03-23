#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyNexus 集成模块性能测试
测试环境管理和插件管理模块的性能指标
"""

import time
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.comfynexus.environment_manager import EnvironmentManager
from modules.comfynexus.plugin_manager import PluginManager

def benchmark(func, name, iterations=3):
    """基准测试函数"""
    times = []
    for i in range(iterations):
        start = time.perf_counter()
        result = func()
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\n{name}")
    print(f"  平均：{avg_time*1000:.1f}ms | 最快：{min_time*1000:.1f}ms | 最慢：{max_time*1000:.1f}ms")
    return avg_time

def main():
    print("=" * 70)
    print("  ComfyNexus 集成模块性能测试")
    print("=" * 70)
    
    env_mgr = EnvironmentManager()
    plugin_mgr = PluginManager()
    
    results = {}
    
    # 环境管理测试
    print("\n📊 环境管理模块测试")
    print("-" * 60)
    
    results['detect_python'] = benchmark(
        lambda: env_mgr.detect_python_version(),
        "Python 版本检测"
    )
    
    results['detect_pytorch'] = benchmark(
        lambda: env_mgr.detect_pytorch_version(),
        "PyTorch 版本检测"
    )
    
    results['check_port'] = benchmark(
        lambda: env_mgr.check_port_conflict(8188),
        "端口冲突检测 (8188)"
    )
    
    results['detect_instances'] = benchmark(
        lambda: env_mgr.detect_comfyui_instances(),
        "ComfyUI 实例发现"
    )
    
    results['system_info'] = benchmark(
        lambda: env_mgr.get_system_info(),
        "完整系统信息"
    )
    
    # 快照测试
    print("\n📸 环境快照测试")
    print("-" * 60)
    
    def create_and_list():
        env_mgr.create_snapshot(f"perf-test-{time.time()}")
        env_mgr.list_snapshots()
    
    results['snapshot_create_list'] = benchmark(
        create_and_list,
        "创建快照 + 列出快照",
        iterations=1
    )
    
    # 插件管理测试
    print("\n🔌 插件管理模块测试")
    print("-" * 60)
    
    results['github_search'] = benchmark(
        lambda: plugin_mgr.search_github("comfyui face", limit=10),
        "GitHub 插件搜索 (comfyui face)",
        iterations=1
    )
    
    # 总结
    print("\n" + "=" * 70)
    print("  性能测试总结")
    print("=" * 70)
    
    print("\n⚡ 快速操作 (< 10ms):")
    fast_ops = [k for k, v in results.items() if v < 0.01]
    if fast_ops:
        for op in fast_ops:
            print(f"  ✅ {op}: {results[op]*1000:.1f}ms")
    
    print("\n🚀 中速操作 (10-100ms):")
    medium_ops = [k for k, v in results.items() if 0.01 <= v < 0.1]
    if medium_ops:
        for op in medium_ops:
            print(f"  ✅ {op}: {results[op]*1000:.1f}ms")
    
    print("\n🌐 网络操作 (> 100ms):")
    slow_ops = [k for k, v in results.items() if v >= 0.1]
    if slow_ops:
        for op in slow_ops:
            print(f"  🌍 {op}: {results[op]*1000:.1f}ms")
    
    print("\n📊 总体评价:")
    avg_all = sum(results.values()) / len(results)
    if avg_all < 0.1:
        print("  ⭐⭐⭐⭐⭐ 优秀 - 所有操作响应迅速")
    elif avg_all < 0.5:
        print("  ⭐⭐⭐⭐ 良好 - 大部分操作响应快速")
    elif avg_all < 1.0:
        print("  ⭐⭐⭐ 中等 - 性能可接受")
    else:
        print("  ⭐⭐ 需要优化 - 部分操作较慢")
    
    print(f"\n  平均响应时间：{avg_all*1000:.1f}ms")
    print(f"  测试项目数：{len(results)}")


if __name__ == "__main__":
    main()
