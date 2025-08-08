# GrowGarden 自动购种机器人

一个用于 Roblox Grow A Garden 游戏的自动化种子购买工具，使用 OCR 技术识别游戏界面并自动购买指定种子。

## 功能特点

- 🤖 自动识别游戏中的种子名称和库存状态
- 🛒 自动购买指定的种子类型
- ⏰ 可设置定时自动执行
- 🖥️ 直观的图形界面
- ⚙️ 灵活的配置选项
- 📊 实时日志显示

## 环境要求

### 系统要求
- macOS / Windows / Linux
- Python 3.7+

### 依赖软件
- **Tesseract OCR** (必需)
  - macOS: `brew install tesseract`
  - Ubuntu: `sudo apt install tesseract-ocr`
  - Windows: [下载安装](https://github.com/UB-Mannheim/tesseract/wiki)

## 快速开始

### 自动安装（推荐）
```bash
chmod +x install.sh
./install.sh
```

### 手动安装
1. **安装 Tesseract OCR**
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt install tesseract-ocr
   
   # Windows - 下载安装包
   # https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

### 快速运行
```bash
# 启动 GUI（推荐）
./run.sh

# 命令行模式
./run.sh --cli

# 或直接运行
python main.py
```

## 使用方法

### GUI 模式（推荐）
```bash
python main.py
```

### 命令行模式
```bash
python main.py --cli
```

## 配置说明

编辑 `config.json` 文件进行配置：

```json
{
  "cron_interval": 10,              // 自动购买间隔（分钟）
  "seed_names": ["Sunflower", "Carrot"],  // 目标种子名称
  "tesseract_cmd": "/opt/homebrew/bin/tesseract",  // Tesseract路径
  "seed_boxes": [...],              // 种子名称识别区域坐标
  "stock_boxes": [...],             // 库存状态识别区域坐标
  "buy_buttons": [...],             // 购买按钮坐标
  "store_hotkey": "f1",             // 打开商店快捷键
  "close_hotkey": "esc"             // 关闭商店快捷键
}
```

### 坐标配置

**重要：** 需要根据你的屏幕分辨率和游戏界面调整坐标参数。

#### 使用坐标配置工具（推荐）
```bash
python coordinate_tool.py
```

使用步骤：
1. 打开游戏商店界面
2. 运行坐标配置工具
3. 点击"截取屏幕"
4. 选择模式并框选相应区域：
   - **种子区域**：拖拽框选种子名称显示区域
   - **库存区域**：拖拽框选库存状态显示区域  
   - **购买按钮**：单击购买按钮位置
5. 点击"保存配置"

#### 手动配置坐标

1. 打开游戏商店界面
2. 使用截图工具获取种子名称、库存状态、购买按钮的坐标
3. 更新 `config.json` 中对应的坐标数组

坐标格式：
- `seed_boxes`: `[left, top, right, bottom]` - 种子名称区域
- `stock_boxes`: `[left, top, right, bottom]` - 库存状态区域  
- `buy_buttons`: `[x, y]` - 购买按钮中心点

## 使用流程

1. **启动游戏**
   - 打开 Roblox GrowGarden
   - 确保游戏处于可操作状态

2. **运行程序**
   - 启动本工具的 GUI 界面
   - 在"配置"选项卡中设置参数
   - 保存配置

3. **开始自动购买**
   - 点击"开始自动购种"按钮
   - 程序将按设定间隔自动执行
   - 查看日志了解执行状态

4. **测试功能**
   - 使用"测试一次"按钮验证配置
   - 根据日志输出调整参数

## 打包为可执行文件

### macOS/Linux
```bash
chmod +x build.sh
./build.sh
```

### Windows
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "GrowGarden-Bot" main.py
```

## 注意事项

### 安全提醒
- ⚠️ 使用自动化工具可能违反游戏服务条款
- ⚠️ 使用前请确认游戏政策
- ⚠️ 本工具仅供学习和研究目的

### 使用建议
- 首次使用先测试功能
- 根据屏幕分辨率调整坐标
- 合理设置购买间隔
- 定期检查日志输出

### 故障排除

**OCR 识别不准确**
- 检查 Tesseract 安装
- 调整识别区域坐标
- 确保游戏界面清晰

**找不到游戏元素**
- 验证坐标配置
- 检查游戏界面是否完整显示
- 确认快捷键设置正确

**程序无响应**
- 检查 Python 环境
- 确认依赖包安装完整
- 查看错误日志

## 技术栈

- **Python 3.7+** - 核心开发语言
- **PyQt5** - GUI 界面框架
- **pytesseract** - OCR 文字识别
- **pyautogui** - 屏幕截图和鼠标控制
- **Pillow** - 图像处理
- **schedule** - 定时任务

## 文件结构

```
growgarden-bot/
├── main.py              # 程序入口
├── gui.py               # GUI 界面
├── seed_buyer.py        # 购买逻辑核心
├── ocr_utils.py         # OCR 工具函数
├── coordinate_tool.py   # 坐标配置工具
├── config.json          # 主配置文件
├── config_demo.json     # 示例配置文件
├── requirements.txt     # Python 依赖
├── install.sh          # 自动安装脚本
├── run.sh              # 启动脚本
├── build.sh            # 打包脚本
└── README.md           # 说明文档
```

## 更新日志

### v1.0 (2025-08-08)
- ✨ 初始版本发布
- 🎯 基础 OCR 识别功能
- 🖥️ GUI 图形界面
- ⚙️ 可配置参数
- 📦 支持打包为可执行文件

## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

这意味着您可以：
- ✅ 自由使用、修改和分发代码
- ✅ 用于商业目的
- ✅ 创建衍生作品
- ✅ 私有使用

唯一要求是在所有副本中保留原始版权声明和许可证文本。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

---

**免责声明**: 本工具仅供学习和研究目的，使用者需自行承担使用风险，开发者不对任何损失承担责任。
