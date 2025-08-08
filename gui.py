import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QSpinBox, 
                             QTextEdit, QGroupBox, QListWidget, QLineEdit,
                             QMessageBox, QTabWidget, QFormLayout, QCheckBox)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon
import pyautogui
from seed_buyer import SeedBuyer

class WorkerThread(QThread):
    """工作线程，用于执行自动购买任务"""
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(bool)  # True: 运行中, False: 已停止
    
    def __init__(self):
        super().__init__()
        self.seed_buyer = SeedBuyer()
        self.seed_buyer.set_log_callback(self.emit_log)
        self.running = False
    
    def emit_log(self, message):
        self.log_signal.emit(message)
    
    def run(self):
        self.running = True
        self.status_signal.emit(True)
        try:
            self.seed_buyer.start_auto_buying()
        except Exception as e:
            self.log_signal.emit(f"工作线程错误: {e}")
        finally:
            self.running = False
            self.status_signal.emit(False)
    
    def stop(self):
        if self.running:
            self.seed_buyer.stop_auto_buying()
            self.running = False

class ConfigTab(QWidget):
    """配置选项卡"""
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 基本设置
        basic_group = QGroupBox("基本设置")
        basic_layout = QFormLayout()
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 120)
        self.interval_spin.setValue(10)
        self.interval_spin.setSuffix(" 分钟")
        basic_layout.addRow("购买间隔:", self.interval_spin)
        
        self.store_hotkey = QLineEdit("f1")
        basic_layout.addRow("打开商店快捷键:", self.store_hotkey)
        
        self.close_hotkey = QLineEdit("esc")
        basic_layout.addRow("关闭商店快捷键:", self.close_hotkey)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # 种子设置
        seed_group = QGroupBox("目标种子")
        seed_layout = QVBoxLayout()
        
        self.seed_list = QListWidget()
        self.seed_list.addItems(["Sunflower", "Carrot", "Potato", "Corn", "Tomato"])
        seed_layout.addWidget(self.seed_list)
        
        seed_button_layout = QHBoxLayout()
        add_seed_btn = QPushButton("添加种子")
        remove_seed_btn = QPushButton("删除种子")
        add_seed_btn.clicked.connect(self.add_seed)
        remove_seed_btn.clicked.connect(self.remove_seed)
        seed_button_layout.addWidget(add_seed_btn)
        seed_button_layout.addWidget(remove_seed_btn)
        seed_layout.addLayout(seed_button_layout)
        
        self.new_seed_input = QLineEdit()
        self.new_seed_input.setPlaceholderText("输入新种子名称...")
        seed_layout.addWidget(self.new_seed_input)
        
        seed_group.setLayout(seed_layout)
        layout.addWidget(seed_group)
        
        # 保存配置按钮
        save_btn = QPushButton("保存配置")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def add_seed(self):
        seed_name = self.new_seed_input.text().strip()
        if seed_name:
            self.seed_list.addItem(seed_name)
            self.new_seed_input.clear()
    
    def remove_seed(self):
        current_row = self.seed_list.currentRow()
        if current_row >= 0:
            self.seed_list.takeItem(current_row)
    
    def save_config(self):
        try:
            # 读取当前配置
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 更新配置
            config['cron_interval'] = self.interval_spin.value()
            config['store_hotkey'] = self.store_hotkey.text()
            config['close_hotkey'] = self.close_hotkey.text()
            
            # 更新种子列表
            seed_names = []
            for i in range(self.seed_list.count()):
                seed_names.append(self.seed_list.item(i).text())
            config['seed_names'] = seed_names
            
            # 保存配置
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            QMessageBox.information(self, "成功", "配置已保存")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置失败: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        self.setWindowTitle("GrowGarden 自动购种机器人 v1.0")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        
        # 主控制选项卡
        main_tab = QWidget()
        self.setup_main_tab(main_tab)
        self.tab_widget.addTab(main_tab, "主控制")
        
        # 配置选项卡
        self.config_tab = ConfigTab(self)
        self.tab_widget.addTab(self.config_tab, "配置")
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
    
    def setup_main_tab(self, tab):
        layout = QVBoxLayout()
        
        # 状态显示
        status_group = QGroupBox("运行状态")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("就绪")
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        status_layout.addWidget(self.status_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 控制按钮
        control_group = QGroupBox("控制")
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("开始自动购种")
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; }")
        self.start_btn.clicked.connect(self.start_automation)
        
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-size: 14px; padding: 10px; }")
        self.stop_btn.clicked.connect(self.stop_automation)
        self.stop_btn.setEnabled(False)
        
        self.test_btn = QPushButton("测试一次")
        self.test_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-size: 14px; padding: 10px; }")
        self.test_btn.clicked.connect(self.test_once)
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.test_btn)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # 日志输出
        log_group = QGroupBox("日志输出")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        # 日志控制按钮
        log_btn_layout = QHBoxLayout()
        clear_log_btn = QPushButton("清空日志")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_btn_layout.addWidget(clear_log_btn)
        log_btn_layout.addStretch()
        log_layout.addLayout(log_btn_layout)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        tab.setLayout(layout)
    
    def load_config(self):
        """加载配置到界面"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 更新配置选项卡
            self.config_tab.interval_spin.setValue(config.get('cron_interval', 10))
            self.config_tab.store_hotkey.setText(config.get('store_hotkey', 'f1'))
            self.config_tab.close_hotkey.setText(config.get('close_hotkey', 'esc'))
            
            # 更新种子列表
            self.config_tab.seed_list.clear()
            self.config_tab.seed_list.addItems(config.get('seed_names', []))
            
        except Exception as e:
            self.add_log(f"加载配置失败: {e}")
    
    def add_log(self, message):
        """添加日志"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.ensureCursorVisible()
    
    def start_automation(self):
        """开始自动化"""
        if self.worker_thread and self.worker_thread.isRunning():
            return
        
        self.worker_thread = WorkerThread()
        self.worker_thread.log_signal.connect(self.add_log)
        self.worker_thread.status_signal.connect(self.update_status)
        self.worker_thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.test_btn.setEnabled(False)
    
    def stop_automation(self):
        """停止自动化"""
        if self.worker_thread:
            self.worker_thread.stop()
            self.worker_thread.wait()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.test_btn.setEnabled(True)
    
    def test_once(self):
        """测试执行一次"""
        self.add_log("开始测试...")
        try:
            buyer = SeedBuyer()
            buyer.set_log_callback(self.add_log)
            buyer.run_buying_cycle()
        except Exception as e:
            self.add_log(f"测试失败: {e}")
    
    def update_status(self, running):
        """更新状态显示"""
        if running:
            self.status_label.setText("🟢 运行中")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("🔴 已停止")
            self.status_label.setStyleSheet("color: red;")
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(self, "确认", "程序正在运行，确定要退出吗？",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.stop_automation()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("GrowGarden Bot")
    app.setApplicationVersion("1.0")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()