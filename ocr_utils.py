import pytesseract
from PIL import Image
import json
import os

# 加载配置
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()

# 设置 Tesseract 路径 (macOS)
if os.path.exists(config['tesseract_cmd']):
    pytesseract.pytesseract.tesseract_cmd = config['tesseract_cmd']
else:
    # 尝试常见的 macOS 安装路径
    possible_paths = [
        '/opt/homebrew/bin/tesseract',
        '/usr/local/bin/tesseract',
        '/usr/bin/tesseract'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

def extract_text(image: Image.Image, lang='eng'):
    """从图像中提取文字"""
    try:
        # 预处理图像以提高 OCR 准确性
        # 转换为灰度
        if image.mode != 'L':
            image = image.convert('L')
        
        # 使用 pytesseract 提取文字
        text = pytesseract.image_to_string(image, lang=lang, config='--psm 8').strip()
        return text
    except Exception as e:
        print(f"OCR 识别错误: {e}")
        return ""

def crop_image(image: Image.Image, box):
    """裁剪图像
    box 为 (left, upper, right, lower) 坐标
    """
    try:
        return image.crop(box)
    except Exception as e:
        print(f"图像裁剪错误: {e}")
        return None

def preprocess_image(image: Image.Image):
    """图像预处理，提高 OCR 识别率"""
    # 转换为灰度
    if image.mode != 'L':
        image = image.convert('L')
    
    # 可以添加更多预处理步骤，如：
    # - 调整对比度
    # - 去噪
    # - 二值化等
    
    return image

def check_stock_status(text):
    """检查库存状态"""
    text_lower = text.lower()
    # 检查是否有库存的关键词
    in_stock_keywords = ['in stock', 'instock', 'available', '有库存', '可购买']
    out_of_stock_keywords = ['out of stock', 'outofstock', 'sold out', '缺货', '售完']
    
    for keyword in in_stock_keywords:
        if keyword in text_lower:
            return True
    
    for keyword in out_of_stock_keywords:
        if keyword in text_lower:
            return False
    
    # 如果没有明确的关键词，尝试检查数字
    import re
    numbers = re.findall(r'\d+', text)
    if numbers:
        try:
            stock_num = int(numbers[0])
            return stock_num > 0
        except ValueError:
            pass
    
    # 默认返回 False（没有库存）
    return False