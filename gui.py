import sys
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.converter import MarkdownConverter

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown转HTML工具")
        self.root.geometry("900x650")  # 调整窗口大小
        
        # 设置窗口最小尺寸
        self.root.minsize(900, 650)
        
        # 配置苹果风格
        self.configure_styles()
        
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

    def configure_styles(self):
        """配置苹果风格的样式"""
        self.root.configure(bg='#f5f5f7')  # 使用苹果浅灰色背景
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置全局字体
        default_font = ('SF Pro Display', 11)  # 使用更大的字体
        self.root.option_add('*Font', default_font)
        
        # 主按钮样式（蓝色背景）
        style.configure('Primary.TButton',
                       padding=(20, 8),
                       font=('SF Pro Display', 11),
                       background='#0066cc',
                       foreground='white',
                       borderwidth=0,
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', '#0077ed'), ('disabled', '#cccccc')],
                 foreground=[('disabled', '#666666')])

        # 次要按钮样式（白色背景）
        style.configure('Secondary.TButton',
                       padding=(15, 6),
                       font=('SF Pro Display', 11),
                       background='#ffffff',
                       foreground='#0066cc',
                       borderwidth=1,
                       relief='solid')
        
        style.map('Secondary.TButton',
                 background=[('active', '#f5f5f7'), ('disabled', '#ffffff')],
                 foreground=[('disabled', '#cccccc')])
        
        # 标签样式
        style.configure('TLabel',
                       font=default_font,
                       background='#ffffff',
                       padding=(8, 8))
        
        # 框架样式
        style.configure('TFrame', background='#ffffff')
        style.configure('Card.TFrame', background='#ffffff', relief='flat')
        
        style.configure('TLabelframe', 
                       background='#ffffff',
                       relief='flat',
                       borderwidth=0)
        
        style.configure('TLabelframe.Label', 
                       font=('SF Pro Display', 13, 'bold'),
                       background='#ffffff',
                       foreground='#1d1d1f',
                       padding=(0, 15))
        
        # 进度条样式
        style.configure('TProgressbar',
                       thickness=6,  # 更细的进度条
                       troughcolor='#e5e5e5',  # 进度条背景色
                       background='#0066cc',  # 进度条颜色
                       borderwidth=0,
                       relief='flat')

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

    def init_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, style='Card.TFrame', padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        # 左侧框架 - 用于目录选择和控制
        left_frame = ttk.LabelFrame(main_frame, text="配置", padding="25")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        # 输入目录选择
        ttk.Label(left_frame, text="输入目录").grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        path_frame1 = ttk.Frame(left_frame, style='Card.TFrame')
        path_frame1.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        ttk.Label(path_frame1, textvariable=self.input_dir, wraplength=300).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(path_frame1, text="选择", style='Secondary.TButton',
                  command=lambda: self.select_directory("input")).grid(row=0, column=1, padx=(15, 0))
        
        # 输出目录选择
        ttk.Label(left_frame, text="输出目录").grid(row=2, column=0, sticky=tk.W, pady=(0, 8))
        path_frame2 = ttk.Frame(left_frame, style='Card.TFrame')
        path_frame2.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        ttk.Label(path_frame2, textvariable=self.output_dir, wraplength=300).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(path_frame2, text="选择", style='Secondary.TButton',
                  command=lambda: self.select_directory("output")).grid(row=0, column=1, padx=(15, 0))
        
        # 模板目录选择
        ttk.Label(left_frame, text="模板目录").grid(row=4, column=0, sticky=tk.W, pady=(0, 8))
        path_frame3 = ttk.Frame(left_frame, style='Card.TFrame')
        path_frame3.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        ttk.Label(path_frame3, textvariable=self.template_dir, wraplength=300).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(path_frame3, text="选择", style='Secondary.TButton',
                  command=lambda: self.select_directory("template")).grid(row=0, column=1, padx=(15, 0))
        
        # 进度条和进度标签
        self.progress_frame = ttk.Frame(left_frame, style='Card.TFrame')
        self.progress_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=20)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        self.progress_label = ttk.Label(self.progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=1, column=0, sticky=tk.W)
        
        self.progress_frame.grid_remove()
        
        # 转换按钮容器
        convert_frame = ttk.Frame(left_frame, style='Card.TFrame')
        convert_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 转换按钮
        convert_button = ttk.Button(convert_frame, text="开始转换", style='Primary.TButton',
                                  command=self.start_conversion)
        convert_button.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 右侧框架 - 用于日志显示
        right_frame = ttk.LabelFrame(main_frame, text="日志", padding="25")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(15, 0))
        
        # 日志文本框
        self.log_text = tk.Text(right_frame, wrap=tk.WORD, width=45, height=25,
                               font=('SF Pro Display', 11),
                               bg='#ffffff',
                               fg='#1d1d1f',
                               relief='flat',
                               padx=15,
                               pady=15,
                               selectbackground='#0066cc',
                               selectforeground='#ffffff')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # 日志操作按钮容器
        log_buttons_frame = ttk.Frame(right_frame, style='Card.TFrame')
        log_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(20, 0), sticky=(tk.W, tk.E))
        
        # 清除日志按钮
        clear_log_button = ttk.Button(log_buttons_frame, text="清除日志", style='Secondary.TButton',
                                    command=lambda: self.log_text.delete(1.0, tk.END))
        clear_log_button.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 配置网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)  # 让日志区域占据更多空间
        main_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        convert_frame.columnconfigure(0, weight=1)  # 让转换按钮自适应宽度
        log_buttons_frame.columnconfigure(0, weight=1)  # 让清除日志按钮自适应宽度
        
        # 设置欢迎信息
        self.log_text.insert(tk.END, "欢迎使用Markdown转HTML工具！\n\n")
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
        if not self.progress_frame.winfo_ismapped():
            self.progress_frame.grid()
            
        progress = (current / total) * 100
        
        # 平滑动画效果
        current_progress = self.progress_bar['value']
        steps = 10
        for i in range(steps + 1):
            intermediate_progress = current_progress + (progress - current_progress) * (i / steps)
            self.progress_bar['value'] = intermediate_progress
            self.progress_var.set(f"正在处理: {filename} ({current}/{total})")
            self.root.update_idletasks()
            if i < steps:
                self.root.after(20)  # 20ms的延迟创建平滑效果
        
        self.add_log(f"正在处理: {filename}")
        self.root.update()
    
    def start_conversion(self):
        # 验证是否选择了所有必需的目录
        if "未选择" in (self.input_dir.get(), self.output_dir.get(), self.template_dir.get()):
            messagebox.showwarning("警告", "请先选择所有必需的目录！")
            return
            
        # 验证模板文件是否存在
        required_templates = ['top.html', 'bottom.html', 'h2.html']
        template_parent_dir = self.template_dir.get()
        
        # 验证父目录是否存在
        if not os.path.exists(template_parent_dir):
            messagebox.showwarning("警告", f"模板父目录不存在：\n{template_parent_dir}")
            return
        
        # 获取父目录下的所有子目录
        template_subdirs = [d for d in os.listdir(template_parent_dir) 
                          if os.path.isdir(os.path.join(template_parent_dir, d))]
        
        if not template_subdirs:
            messagebox.showwarning("警告", "模板父目录下没有子文件夹！")
            return
        
        # 在每个子目录中查找模板文件
        template_dir = None
        for subdir in template_subdirs:
            subdir_path = os.path.join(template_parent_dir, subdir)
            # 检查该子目录是否包含所有必需的模板文件
            if all(os.path.exists(os.path.join(subdir_path, f)) for f in required_templates):
                template_dir = subdir_path
                break
        
        if not template_dir:
            messagebox.showwarning("警告", 
                                 f"在子文件夹中未找到完整的模板文件集！\n需要的文件：{', '.join(required_templates)}")
            return
            
        try:
            # 创建转换器，使用找到的模板目录
            converter = MarkdownConverter(template_dir)
            
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