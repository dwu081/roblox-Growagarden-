#!/bin/bash
# GrowGarden Bot 打包脚本 (macOS)

echo "🚀 开始打包 GrowGarden Bot..."
echo "================================"

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 检测到虚拟环境: $VIRTUAL_ENV"
else
    echo "⚠️  建议在虚拟环境中运行打包"
fi

# 安装 pyinstaller
echo "📦 安装 pyinstaller..."
pip install pyinstaller

# 清理之前的构建
if [ -d "build" ]; then
    echo "🧹 清理 build 目录..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "🧹 清理 dist 目录..."
    rm -rf dist
fi

if [ -f "GrowGarden-Bot.spec" ]; then
    echo "🧹 删除旧的 spec 文件..."
    rm GrowGarden-Bot.spec
fi

echo "🔨 正在打包应用程序..."

# 打包为 macOS 应用
pyinstaller --onefile \
    --windowed \
    --name "GrowGarden-Bot" \
    --add-data "config.json:." \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=pytesseract \
    --hidden-import=pyautogui \
    --hidden-import=PIL \
    --hidden-import=PIL.Image \
    --hidden-import=schedule \
    --collect-submodules=PyQt5 \
    --noconfirm \
    main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 打包成功！"
    echo "📁 可执行文件位置: dist/GrowGarden-Bot"
    echo ""
    echo "📋 使用说明:"
    echo "1. 确保已安装 Tesseract OCR"
    echo "2. 运行: ./dist/GrowGarden-Bot"
    echo ""
    echo "🔧 如需创建 .app 包，可运行："
    echo "   pyinstaller --onedir --windowed --name 'GrowGarden Bot' main.py"
    echo ""
else
    echo "❌ 打包失败！请检查错误信息"
    exit 1
fi
