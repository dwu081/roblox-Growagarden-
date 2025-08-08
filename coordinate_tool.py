#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坐标配置工具
帮助用户获取游戏界面中种子区域、库存区域和购买按钮的坐标
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
from PIL import Image, ImageTk
import json
import os

class CoordinateConfig:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("坐标配置工具")
        self.root.geometry("800x600")
        
        self.screenshot = None
        self.photo = None
        self.canvas = None
        
        # 配置数据
        self.seed_boxes = []
        self.stock_boxes = []
        self.buy_buttons = []
        
        # 当前选择模式
        self.mode = tk.StringVar(value="seed")
        
        # 拖拽状态
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # 顶部控制区
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # 截图按钮
        ttk.Button(control_frame, text="截取屏幕", command=self.take_screenshot).pack(side="left", padx=5)
        
        # 模式选择
        ttk.Label(control_frame, text="选择模式:").pack(side="left", padx=(20, 5))
        ttk.Radiobutton(control_frame, text="种子区域", variable=self.mode, value="seed").pack(side="left")
        ttk.Radiobutton(control_frame, text="库存区域", variable=self.mode, value="stock").pack(side="left")
        ttk.Radiobutton(control_frame, text="购买按钮", variable=self.mode, value="button").pack(side="left")
        
        # 保存按钮
        ttk.Button(control_frame, text="保存配置", command=self.save_config).pack(side="right", padx=5)
        ttk.Button(control_frame, text="清空选择", command=self.clear_selections).pack(side="right", padx=5)
        
        # 画布区域
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # 底部信息区
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="请先截取屏幕，然后选择相应区域")
        self.info_label.pack()
        
        # 配置显示区
        config_frame = ttk.LabelFrame(self.root, text="当前配置")
        config_frame.pack(fill="x", padx=10, pady=5)
        
        self.config_text = tk.Text(config_frame, height=8, font=("Courier", 10))
        self.config_text.pack(fill="x", padx=5, pady=5)
    
    def take_screenshot(self):
        """截取屏幕"""
        try:
            # 最小化窗口
            self.root.withdraw()
            
            # 等待窗口最小化
            self.root.after(1000, self._do_screenshot)
            
        except Exception as e:
            messagebox.showerror("错误", f"截图失败: {e}")
            self.root.deiconify()
    
    def _do_screenshot(self):
        """执行截图"""
        try:
            self.screenshot = pyautogui.screenshot()
            
            # 调整图片大小以适应画布
            canvas_width = 700
            canvas_height = 400
            
            img_width, img_height = self.screenshot.size
            scale = min(canvas_width / img_width, canvas_height / img_height)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            resized_img = self.screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_img)
            
            # 显示图片
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            self.info_label.config(text="截图完成！请选择区域。种子区域用绿色框，库存区域用蓝色框，购买按钮用红色点。")
            
            # 存储缩放比例
            self.scale_x = img_width / new_width
            self.scale_y = img_height / new_height
            
        except Exception as e:
            messagebox.showerror("错误", f"处理截图失败: {e}")
        finally:
            self.root.deiconify()
    
    def on_canvas_click(self, event):
        """鼠标点击事件"""
        if self.screenshot is None:
            return
        
        if self.mode.get() == "button":
            # 购买按钮模式：单击添加点
            x = int(event.x * self.scale_x)
            y = int(event.y * self.scale_y)
            
            self.buy_buttons.append([x, y])
            
            # 在画布上显示红色圆点
            self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, 
                                  fill="red", outline="red")
            
            self.update_config_display()
        else:
            # 区域选择模式：开始拖拽
            self.start_x = event.x
            self.start_y = event.y
    
    def on_canvas_drag(self, event):
        """鼠标拖拽事件"""
        if self.screenshot is None or self.mode.get() == "button":
            return
        
        if self.start_x is not None and self.start_y is not None:
            # 删除之前的临时矩形
            if self.current_rect:
                self.canvas.delete(self.current_rect)
            
            # 绘制新的矩形
            color = "green" if self.mode.get() == "seed" else "blue"
            self.current_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline=color, width=2, fill="", stipple="gray50"
            )
    
    def on_canvas_release(self, event):
        """鼠标释放事件"""
        if self.screenshot is None or self.mode.get() == "button":
            return
        
        if self.start_x is not None and self.start_y is not None:
            # 计算实际坐标
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            # 转换为原始图片坐标
            real_x1 = int(x1 * self.scale_x)
            real_y1 = int(y1 * self.scale_y)
            real_x2 = int(x2 * self.scale_x)
            real_y2 = int(y2 * self.scale_y)
            
            # 保存坐标
            if self.mode.get() == "seed":
                self.seed_boxes.append([real_x1, real_y1, real_x2, real_y2])
            elif self.mode.get() == "stock":
                self.stock_boxes.append([real_x1, real_y1, real_x2, real_y2])
            
            self.update_config_display()
            
            # 重置拖拽状态
            self.start_x = None
            self.start_y = None
            self.current_rect = None
    
    def clear_selections(self):
        """清空选择"""
        self.seed_boxes.clear()
        self.stock_boxes.clear()
        self.buy_buttons.clear()
        
        if self.screenshot:
            # 重新显示截图
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        
        self.update_config_display()
    
    def update_config_display(self):
        """更新配置显示"""
        config = {
            "seed_boxes": self.seed_boxes,
            "stock_boxes": self.stock_boxes,
            "buy_buttons": self.buy_buttons
        }
        
        config_text = json.dumps(config, indent=2, ensure_ascii=False)
        
        self.config_text.delete(1.0, tk.END)
        self.config_text.insert(1.0, config_text)
    
    def save_config(self):
        """保存配置到文件"""
        try:
            # 读取现有配置
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 更新坐标配置
            config['seed_boxes'] = self.seed_boxes
            config['stock_boxes'] = self.stock_boxes
            config['buy_buttons'] = self.buy_buttons
            
            # 保存配置
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("成功", "配置已保存到 config.json")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")
    
    def run(self):
        """运行工具"""
        self.root.mainloop()

def main():
    print("坐标配置工具")
    print("=" * 30)
    print("使用说明:")
    print("1. 首先打开游戏商店界面")
    print("2. 点击'截取屏幕'按钮")
    print("3. 选择相应模式并框选区域:")
    print("   - 种子区域: 拖拽框选种子名称区域")
    print("   - 库存区域: 拖拽框选库存状态区域")
    print("   - 购买按钮: 单击购买按钮位置")
    print("4. 点击'保存配置'")
    print()
    
    app = CoordinateConfig()
    app.run()

if __name__ == "__main__":
    main()
