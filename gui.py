import sys
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.converter import MarkdownConverter
from src.tkdnd import add_drag_n_drop_support

# 定义拖放常量
DND_FILES = 'DND_Files'

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown转HTML工具")
        self.root.geometry("600x500")
        
        # 添加拖放支持
        add_drag_n_drop_support(self.root)
        
        # 配置文件路径
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        
        # 初始化路径变量
        self.input_dir = tk.StringVar(value="未选择")
        self.output_dir = tk.StringVar(value="未选择")
        self.template_dir = tk.StringVar(value="未选择")
        
        # 初始化进度变量
        self.progress_var = tk.StringVar(value="")
        
        # 加载上次的配置
        self.load_config()
        
        # 创建主界面
        self.init_ui()
        
        # 绑定关闭窗口事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        try:
            # 设置文件拖放
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)
        except:
            self.add_log("提示：拖放功能不可用，请使用选择按钮选择目录")

    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if config.get('input_dir'):
                        self.input_dir.set(config['input_dir'])
                    if config.get('output_dir'):
                        self.output_dir.set(config['output_dir'])
                    if config.get('template_dir'):
                        self.template_dir.set(config['template_dir'])
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")

    def save_config(self):
        """保存配置文件"""
        try:
            config = {
                'input_dir': self.input_dir.get() if self.input_dir.get() != "未选择" else "",
                'output_dir': self.output_dir.get() if self.output_dir.get() != "未选择" else "",
                'template_dir': self.template_dir.get() if self.template_dir.get() != "未选择" else ""
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")

    def on_closing(self):
        """窗口关闭时保存配置"""
        self.save_config()
        self.root.destroy()

    def handle_drop(self, event):
        """处理文件拖放"""
        files = self.root.tk.splitlist(event.data)
        if files:
            path = files[0]  # 获取第一个拖放的路径
            if os.path.isdir(path):
                self.input_dir.set(path)
            else:
                messagebox.showinfo("提示", "请拖放文件夹而不是文件")

    def init_ui(self):
        # 设置样式
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 左侧框架 - 用于目录选择和控制
        left_frame = ttk.LabelFrame(main_frame, text="配置", padding="5")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 输入目录选择
        ttk.Label(left_frame, text="输入目录：").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(left_frame, textvariable=self.input_dir, wraplength=200).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(left_frame, text="选择", 
                  command=lambda: self.select_directory("input")).grid(row=0, column=2, padx=5)
        
        # 输出目录选择
        ttk.Label(left_frame, text="输出目录：").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(left_frame, textvariable=self.output_dir, wraplength=200).grid(row=1, column=1, sticky=tk.W)
        ttk.Button(left_frame, text="选择", 
                  command=lambda: self.select_directory("output")).grid(row=1, column=2, padx=5)
        
        # 模板目录选择
        ttk.Label(left_frame, text="模板目录：").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(left_frame, textvariable=self.template_dir, wraplength=200).grid(row=2, column=1, sticky=tk.W)
        ttk.Button(left_frame, text="选择", 
                  command=lambda: self.select_directory("template")).grid(row=2, column=2, padx=5)
        
        # 进度条和进度标签
        progress_frame = ttk.Frame(left_frame)
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=1, column=0, padx=5)
        
        progress_frame.grid_remove()
        self.progress_frame = progress_frame
        
        # 转换按钮
        convert_button = ttk.Button(left_frame, text="开始转换", 
                                  command=self.start_conversion)
        convert_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        # 右侧框架 - 用于日志显示
        right_frame = ttk.LabelFrame(main_frame, text="日志", padding="5")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 日志文本框
        self.log_text = tk.Text(right_frame, wrap=tk.WORD, width=40, height=20)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # 清除日志按钮
        clear_log_button = ttk.Button(right_frame, text="清除日志", 
                                    command=lambda: self.log_text.delete(1.0, tk.END))
        clear_log_button.grid(row=1, column=0, columnspan=2, pady=5)
        
        # 配置网格权重
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # 设置拖放提示
        self.log_text.insert(tk.END, "欢迎使用Markdown转HTML工具！\n")
        self.log_text.insert(tk.END, "提示：您可以直接将文件夹拖放到窗口来设置输入目录。\n\n")
        self.log_text.see(tk.END)

    def add_log(self, message):
        """添加日志信息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def select_directory(self, dir_type):
        directory = filedialog.askdirectory(title="选择文件夹")
        if directory:
            if dir_type == "input":
                self.input_dir.set(directory)
            elif dir_type == "output":
                self.output_dir.set(directory)
            else:  # template
                self.template_dir.set(directory)
    
    def update_progress(self, current, total, filename):
        """更新进度条和进度标签"""
        progress = (current / total) * 100
        self.progress_bar['value'] = progress
        self.progress_var.set(f"{current}/{total} - {filename}")
        self.add_log(f"正在处理: {filename}")
        self.root.update()
    
    def start_conversion(self):
        # 验证是否选择了所有必需的目录
        if "未选择" in (self.input_dir.get(), self.output_dir.get(), self.template_dir.get()):
            messagebox.showwarning("警告", "请先选择所有必需的目录！")
            return
            
        # 验证模板文件是否存在
        required_templates = ['top.html', 'bottom.html', 'h2.html']
        missing_templates = [f for f in required_templates 
                           if not os.path.exists(os.path.join(self.template_dir.get(), f))]
        if missing_templates:
            messagebox.showwarning("警告", 
                                 f"模板目录中缺少以下文件：\n{', '.join(missing_templates)}")
            return
            
        try:
            # 创建转换器
            converter = MarkdownConverter(self.template_dir.get())
            
            # 显示进度条
            self.progress_frame.grid()
            self.progress_bar['value'] = 0
            self.progress_var.set("准备开始...")
            self.add_log("开始转换...")
            
            # 开始转换
            success_count, fail_count = converter.convert_directory(
                self.input_dir.get(), 
                self.output_dir.get(),
                self.update_progress
            )
            
            # 隐藏进度条
            self.progress_frame.grid_remove()
            
            # 显示结果
            result_message = f"转换完成！\n成功：{success_count} 个文件\n失败：{fail_count} 个文件"
            messagebox.showinfo("转换完成", result_message)
            self.add_log(result_message)
            
        except Exception as e:
            error_message = f"转换过程中发生错误：\n{str(e)}"
            messagebox.showerror("错误", error_message)
            self.add_log(f"错误：{str(e)}")
            self.progress_frame.grid_remove()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main() 