#!/bin/bash
# GrowGarden Bot 安装脚本

echo "🌱 GrowGarden 自动购种机器人 - 安装脚本"
echo "============================================"
echo ""

# 检查操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
else
    OS="Unknown"
fi

echo "🖥️  检测到操作系统: $OS"
echo ""

# 检查 Python
echo "🐍 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    echo "✅ Python3 已安装: $PYTHON_VERSION"
else
    echo "❌ 未找到 Python3"
    echo "请先安装 Python 3.7+"
    exit 1
fi

# 检查 pip
echo "📦 检查 pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 已安装"
else
    echo "❌ 未找到 pip3"
    exit 1
fi

# 检查 Tesseract OCR
echo "🔍 检查 Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version | head -n1 | cut -d ' ' -f 2)
    echo "✅ Tesseract OCR 已安装: $TESSERACT_VERSION"
else
    echo "⚠️  未找到 Tesseract OCR"
    echo ""
    if [[ "$OS" == "macOS" ]]; then
        echo "安装命令: brew install tesseract"
    elif [[ "$OS" == "Linux" ]]; then
        echo "安装命令: sudo apt install tesseract-ocr"
    fi
    echo ""
    read -p "是否继续安装 Python 依赖? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建虚拟环境
echo "🏗️  创建虚拟环境..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ 虚拟环境已创建"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source .venv/bin/activate

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 安装 Python 依赖..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 安装完成！"
    echo ""
    echo "📋 使用方法:"
    echo "1. 运行 GUI 版本: ./run.sh"
    echo "2. 运行命令行版本: ./run.sh --cli"
    echo "3. 配置坐标: python coordinate_tool.py"
    echo "4. 打包程序: ./build.sh"
    echo ""
    echo "📖 更多信息请查看 README.md"
else
    echo "❌ 安装失败！"
    exit 1
fi
