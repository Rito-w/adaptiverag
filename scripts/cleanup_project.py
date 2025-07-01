#!/usr/bin/env python3
"""
项目清理脚本
删除缓存文件、临时文件和不必要的文件
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_project():
    """清理项目文件"""
    project_root = Path(__file__).parent.parent
    
    print("🧹 开始清理项目...")
    
    # 要删除的文件模式
    patterns_to_delete = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo", 
        "**/*.pyd",
        "**/.pytest_cache",
        "**/.coverage",
        "**/htmlcov",
        "**/*.log",
        "**/temp",
        "**/tmp",
        "**/.DS_Store",
        "**/Thumbs.db"
    ]
    
    # 要删除的具体文件
    files_to_delete = [
        ".coverage",
        "coverage.xml",
        "pytest.ini",
        "setup.cfg"
    ]
    
    deleted_count = 0
    
    # 删除匹配模式的文件和目录
    for pattern in patterns_to_delete:
        for path in project_root.glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                    print(f"🗑️ 删除文件: {path.relative_to(project_root)}")
                elif path.is_dir():
                    shutil.rmtree(path)
                    print(f"🗑️ 删除目录: {path.relative_to(project_root)}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 删除失败 {path}: {e}")
    
    # 删除具体文件
    for filename in files_to_delete:
        file_path = project_root / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"🗑️ 删除文件: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 删除失败 {filename}: {e}")
    
    print(f"✅ 清理完成，共删除 {deleted_count} 个文件/目录")

def cleanup_experiments():
    """清理实验结果（可选）"""
    project_root = Path(__file__).parent.parent
    experiments_dir = project_root / "experiments"
    
    if experiments_dir.exists():
        response = input("🤔 是否清理实验结果目录？(y/N): ")
        if response.lower() == 'y':
            try:
                shutil.rmtree(experiments_dir)
                experiments_dir.mkdir()
                (experiments_dir / ".gitkeep").touch()
                print("🗑️ 实验结果已清理")
            except Exception as e:
                print(f"❌ 清理实验结果失败: {e}")

def show_project_size():
    """显示项目大小"""
    project_root = Path(__file__).parent.parent
    
    total_size = 0
    file_count = 0
    
    for path in project_root.rglob("*"):
        if path.is_file():
            try:
                size = path.stat().st_size
                total_size += size
                file_count += 1
            except:
                pass
    
    # 转换为可读格式
    if total_size < 1024:
        size_str = f"{total_size} B"
    elif total_size < 1024 * 1024:
        size_str = f"{total_size / 1024:.1f} KB"
    elif total_size < 1024 * 1024 * 1024:
        size_str = f"{total_size / (1024 * 1024):.1f} MB"
    else:
        size_str = f"{total_size / (1024 * 1024 * 1024):.1f} GB"
    
    print(f"📊 项目统计: {file_count} 个文件, 总大小 {size_str}")

if __name__ == "__main__":
    print("🧹 AdaptiveRAG 项目清理工具")
    print("=" * 40)
    
    show_project_size()
    print()
    
    cleanup_project()
    print()
    
    cleanup_experiments()
    print()
    
    show_project_size()
    print()
    
    print("🎉 清理完成！")
