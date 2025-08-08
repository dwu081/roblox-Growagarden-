# 快速使用指南

## 🚀 环境已就绪！

虚拟环境和所有依赖都已经配置完成，您可以直接开始使用。

## 🎯 运行方式

### 方式一：使用启动脚本（推荐）
```bash
# 启动 GUI 版本
./run.sh

# 启动命令行版本  
./run.sh --cli
```

### 方式二：手动激活虚拟环境
```bash
# 进入项目目录
cd "/Users/wudi/Documents/pychame/roblox OCR"

# 激活虚拟环境
source .venv/bin/activate

# 运行程序
python main.py        # GUI 版本
python main.py --cli  # 命令行版本
```

### 方式三：坐标配置工具
```bash
# 激活虚拟环境后运行
source .venv/bin/activate
python coordinate_tool.py
```

## 📋 使用步骤

1. **首次使用 - 配置坐标**
   ```bash
   source .venv/bin/activate
   python coordinate_tool.py
   ```
   - 打开游戏商店界面
   - 截取屏幕
   - 框选种子区域、库存区域
   - 点击购买按钮位置
   - 保存配置

2. **正常使用**
   ```bash
   ./run.sh
   ```
   - 在"配置"选项卡设置参数
   - 点击"开始自动购种"

## ⚠️ 重要提醒

- 虚拟环境已经配置在 `.venv` 目录中
- 所有 Python 依赖都已安装完成
- Tesseract OCR 已检测到并配置
- 使用前请先配置游戏界面坐标

## 🔧 如果遇到问题

```bash
# 重新安装依赖
source .venv/bin/activate
pip install -r requirements.txt

# 检查环境
python -c "import PyQt5, pytesseract, pyautogui, PIL, schedule; print('✅ 所有依赖正常')"
```
