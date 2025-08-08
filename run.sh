#!/bin/bash
# GrowGarden Bot 启动脚本

echo "🌱 GrowGarden 自动购种机器人"
echo "==============================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python"
    exit 1
fi

# 检查 Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  未找到 Tesseract OCR"
    echo "请安装 Tesseract: brew install tesseract"
    echo ""
    read -p "是否继续运行? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查虚拟环境
if [ -d ".venv" ]; then
    echo "🔍 激活虚拟环境..."
    source .venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "⚠️  未找到虚拟环境，使用系统 Python"
fi

# 检查依赖
echo "🔍 检查 Python 依赖..."
if ! python -c "import PyQt5, pytesseract, pyautogui, PIL, schedule" 2>/dev/null; then
    echo "📦 安装依赖包..."
    pip install -r requirements.txt
fi

echo "🚀 启动程序..."
echo ""

# 运行程序
python main.py "$@"
