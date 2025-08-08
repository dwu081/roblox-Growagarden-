#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GrowGarden 自动购种机器人
一个用于 Roblox GrowGarden 游戏的自动化种子购买工具

作者: AI Assistant
版本: 1.0
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """检查依赖包是否已安装"""
    try:
        import PyQt5
        import pytesseract
        import pyautogui
        from PIL import Image
        import schedule
        return True
    except ImportError as e:
        print(f"缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_tesseract():
    """检查 Tesseract OCR 是否已安装"""
    import subprocess
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Tesseract OCR 已安装: {result.stdout.split()[1]}")
            return True
        else:
            return False
    except FileNotFoundError:
        print("未找到 Tesseract OCR")
        print("请安装 Tesseract OCR:")
        print("macOS: brew install tesseract")
        print("Ubuntu: sudo apt install tesseract-ocr")
        print("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def run_gui():
    """运行 GUI 界面"""
    from gui import main
    main()

def run_cli():
    """运行命令行版本"""
    from seed_buyer import SeedBuyer
    
    print("=" * 50)
    print("GrowGarden 自动购种机器人 - 命令行版本")
    print("=" * 50)
    
    buyer = SeedBuyer()
    
    print("选择运行模式:")
    print("1. 测试一次")
    print("2. 自动运行")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        print("开始测试...")
        buyer.run_buying_cycle()
    elif choice == "2":
        print("开始自动运行...")
        print("按 Ctrl+C 停止")
        try:
            buyer.start_auto_buying()
        except KeyboardInterrupt:
            print("\n程序已停止")
    else:
        print("无效选择")

def main():
    print("GrowGarden 自动购种机器人 v1.0")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查 Tesseract
    if not check_tesseract():
        print("警告: Tesseract OCR 未正确安装，OCR 功能可能无法工作")
        response = input("是否继续运行? (y/N): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--cli', '-c']:
            run_cli()
            return
        elif sys.argv[1] in ['--help', '-h']:
            print("使用方法:")
            print("  python main.py        # 运行 GUI 版本")
            print("  python main.py --cli  # 运行命令行版本")
            print("  python main.py --help # 显示帮助")
            return
    
    # 默认运行 GUI
    try:
        run_gui()
    except ImportError:
        print("GUI 依赖缺失，切换到命令行模式...")
        run_cli()

if __name__ == "__main__":
    main()