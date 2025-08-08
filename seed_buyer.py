import pyautogui
from PIL import Image
import time
import json
import os
from ocr_utils import extract_text, crop_image, check_stock_status, load_config

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class SeedBuyer:
    def __init__(self):
        self.config = load_config()
        self.running = False
        self.log_callback = None
    
    def set_log_callback(self, callback):
        """设置日志回调函数"""
        self.log_callback = callback
    
    def log(self, message):
        """记录日志"""
        print(message)
        if self.log_callback:
            self.log_callback(message)
    
    def open_store(self):
        """打开商店"""
        try:
            self.log("正在打开商店...")
            pyautogui.press(self.config['store_hotkey'])
            time.sleep(2)  # 等待商店界面加载
            return True
        except Exception as e:
            self.log(f"打开商店失败: {e}")
            return False
    
    def close_store(self):
        """关闭商店"""
        try:
            pyautogui.press(self.config['close_hotkey'])
            time.sleep(1)
            self.log("商店已关闭")
        except Exception as e:
            self.log(f"关闭商店失败: {e}")
    
    def take_screenshot(self):
        """截取屏幕"""
        try:
            screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            self.log(f"截图失败: {e}")
            return None
    
    def identify_seeds(self, screenshot):
        """识别屏幕上的种子"""
        seeds_found = []
        
        for idx, box in enumerate(self.config['seed_boxes']):
            try:
                # 裁剪种子名称区域
                seed_img = crop_image(screenshot, box)
                if seed_img is None:
                    continue
                
                # OCR 识别种子名称
                seed_name = extract_text(seed_img)
                
                if seed_name:
                    self.log(f"识别到种子 #{idx+1}: {seed_name}")
                    
                    # 检查是否是目标种子
                    for target_seed in self.config['seed_names']:
                        if target_seed.lower() in seed_name.lower():
                            seeds_found.append({
                                'index': idx,
                                'name': seed_name,
                                'target': target_seed,
                                'box': box
                            })
                            break
                
            except Exception as e:
                self.log(f"识别种子 #{idx+1} 时出错: {e}")
        
        return seeds_found
    
    def check_seed_stock(self, screenshot, seed_index):
        """检查种子库存状态"""
        try:
            if seed_index >= len(self.config['stock_boxes']):
                return False
            
            stock_box = self.config['stock_boxes'][seed_index]
            stock_img = crop_image(screenshot, stock_box)
            
            if stock_img is None:
                return False
            
            stock_text = extract_text(stock_img)
            self.log(f"库存状态文本: {stock_text}")
            
            return check_stock_status(stock_text)
            
        except Exception as e:
            self.log(f"检查库存失败: {e}")
            return False
    
    def buy_seed(self, seed_index):
        """购买种子"""
        try:
            if seed_index >= len(self.config['buy_buttons']):
                self.log(f"没有找到第 {seed_index+1} 个购买按钮")
                return False
            
            x, y = self.config['buy_buttons'][seed_index]
            
            # 点击购买按钮
            pyautogui.click(x, y)
            self.log(f"已点击购买按钮 ({x}, {y})")
            
            time.sleep(1)  # 等待购买动画
            return True
            
        except Exception as e:
            self.log(f"购买种子失败: {e}")
            return False
    
    def run_buying_cycle(self):
        """执行一次完整的购买周期"""
        try:
            self.log("=" * 50)
            self.log("开始新的购买周期...")
            
            # 打开商店
            if not self.open_store():
                return False
            
            # 截取屏幕
            screenshot = self.take_screenshot()
            if screenshot is None:
                self.close_store()
                return False
            
            # 识别种子
            seeds_found = self.identify_seeds(screenshot)
            
            if not seeds_found:
                self.log("没有找到目标种子")
                self.close_store()
                return False
            
            # 检查库存并购买
            purchases_made = 0
            for seed in seeds_found:
                seed_idx = seed['index']
                seed_name = seed['name']
                target_name = seed['target']
                
                self.log(f"检查 {target_name} ({seed_name}) 的库存...")
                
                if self.check_seed_stock(screenshot, seed_idx):
                    self.log(f"{target_name} 有库存，正在购买...")
                    
                    if self.buy_seed(seed_idx):
                        self.log(f"✅ 成功购买 {target_name}")
                        purchases_made += 1
                    else:
                        self.log(f"❌ 购买 {target_name} 失败")
                else:
                    self.log(f"❌ {target_name} 缺货")
            
            # 关闭商店
            self.close_store()
            
            self.log(f"本轮购买完成，共购买了 {purchases_made} 种种子")
            return True
            
        except Exception as e:
            self.log(f"购买周期执行失败: {e}")
            self.close_store()
            return False
    
    def start_auto_buying(self):
        """开始自动购买（定时执行）"""
        import schedule
        
        self.running = True
        self.log(f"自动购买已启动，间隔: {self.config['cron_interval']} 分钟")
        
        # 设置定时任务
        schedule.every(self.config['cron_interval']).minutes.do(self.run_buying_cycle)
        
        # 立即执行一次
        self.run_buying_cycle()
        
        # 定时循环
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop_auto_buying(self):
        """停止自动购买"""
        self.running = False
        self.log("自动购买已停止")

# 单独运行测试
if __name__ == "__main__":
    buyer = SeedBuyer()
    buyer.run_buying_cycle()