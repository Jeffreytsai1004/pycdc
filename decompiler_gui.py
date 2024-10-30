import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys
import shutil
import time
from ctypes import windll, byref, sizeof, c_int, Structure, WINFUNCTYPE, POINTER
from ctypes.wintypes import BOOL, HWND, LPARAM, DWORD, LPWSTR, LPCWSTR

# 定义Windows API需要的结构和常量
class WINDOWINFO(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("rcWindow", DWORD * 4),
        ("rcClient", DWORD * 4),
        ("dwStyle", DWORD),
        ("dwExStyle", DWORD),
        ("dwWindowStatus", DWORD),
        ("cxWindowBorders", c_int),
        ("cyWindowBorders", c_int),
        ("atomWindowType", c_int),
        ("wCreatorVersion", c_int)
    ]

class SingletonGUI:
    _instance = None
    
    @classmethod
    def close_existing_window(cls):
        """查找并关闭已存在的窗口"""
        def enum_window_callback(hwnd, _):
            length = windll.user32.GetWindowTextLengthW(hwnd)
            buff = LPWSTR(" " * length)
            windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            
            if title == "Python 反编译工具" and windll.user32.IsWindowVisible(hwnd):
                windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
            return True
        
        WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
        enum_func = WNDENUMPROC(enum_window_callback)
        windll.user32.EnumWindows(enum_func, 0)

class DecompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 反编译工具")
        self.root.geometry("900x600")
        
        # 设置主题
        ctk.set_appearance_mode("dark")  # 设置深色主题
        
        # 创建自定义主题 JSON 文件
        theme_path = "custom_theme.json"
        custom_theme = {
            "CTk": {
                "fg_color": ["#FAF3E0", "#2B2B2B"],  # 奶油色背景
                "top_fg_color": ["#FAF3E0", "#2B2B2B"],
                "border_color": ["#FFF5E6", "#4A4A4A"],  # 奶白色边框
                "corner_radius": 10
            },
            "CTkFrame": {
                "fg_color": ["#FFDFD3", "#363636"],  # 淡粉色框架
                "top_fg_color": ["#FFDFD3", "#363636"],
                "border_color": ["#FFF5E6", "#4A4A4A"],  # 奶白色边框
                "border_width": 2,
                "corner_radius": 8
            },
            "CTkButton": {
                "fg_color": ["#FFF5E4", "#FFF5E4"],  # 奶白色背景
                "hover_color": ["#FFE6D0", "#FFE6D0"],  # 悬停时稍深的奶白色
                "border_color": ["#FFD7B5", "#FFD7B5"],  # 边框颜色
                "text_color": ["#8B4513", "#8B4513"],  # 深棕色文字
                "text_color_disabled": ["#999999", "#666666"],
                "border_width": 0,
                "corner_radius": 12,
                "height": 40,
                "font": ("Microsoft YaHei UI", 13)
            },
            "CTkEntry": {
                "fg_color": ["#FFFFFF", "#2B2B2B"],
                "border_color": ["#FFF5E6", "#4A4A4A"],  # 奶白色边框
                "text_color": ["#2B2B2B", "#FFFFFF"],
                "placeholder_text_color": ["#999999", "#666666"],
                "corner_radius": 6,
                "height": 35,
                "border_width": 2
            },
            "CTkTextbox": {
                "fg_color": ["#FFFFFF", "#2B2B2B"],
                "border_color": ["#FFF5E6", "#4A4A4A"],  # 奶白色边框
                "text_color": ["#2B2B2B", "#FFFFFF"],
                "border_width": 2,
                "corner_radius": 6,
                "scrollbar_button_color": ["#E26585", "#E26585"],  # 滚动条按钮颜色
                "scrollbar_button_hover_color": ["#D15575", "#D15575"]  # 滚动条悬停颜色
            },
            "CTkLabel": {
                "fg_color": "transparent",
                "text_color": ["#2B2B2B", "#FFFFFF"],
                "corner_radius": 0,
                "height": 35,
                "font": ("Arial", 12)
            },
            "CTkScrollbar": {
                "fg_color": "transparent",
                "button_color": ["#E26585", "#E26585"],  # 滚动条按钮颜色
                "button_hover_color": ["#D15575", "#D15575"],  # 滚动条悬停颜色
                "corner_radius": 1000,
                "border_spacing": 4,
                "minimum_pixel_length": 20
            },
            "DropdownMenu": {
                "fg_color": ["#FFDFD3", "#363636"],
                "hover_color": ["#E26585", "#E26585"],
                "text_color": ["#2B2B2B", "#FFFFFF"],
                "text_color_disabled": ["#999999", "#666666"]
            },
            "CTkFont": {
                "family": "Arial",
                "size": 13,
                "weight": "normal"
            }
        }
        
        # 将主题写入临时文件
        import json
        import tempfile
        import atexit
        
        temp_dir = tempfile.mkdtemp()
        theme_path = os.path.join(temp_dir, "custom_theme.json")
        
        with open(theme_path, "w") as f:
            json.dump(custom_theme, f, indent=2)
        
        # 注册程序退出时删除临时文件
        atexit.register(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        
        # 设置主题
        ctk.set_default_color_theme(theme_path)
        
        # 获取程序运行路径
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))

        # 设置窗口图标
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe，从资源目录获取图标
            icon_path = os.path.join(sys._MEIPASS, 'icon', 'logo.ico')
        else:
            # 如果是开发环境，从当前目录获取图标
            icon_path = os.path.join('icon', 'logo.ico')
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(default=icon_path)
            except Exception as e:
                self.log_message(f"加载图标失败: {str(e)}")
        
        # 主容器
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # 输入设置框
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # 使用 grid 布局替代 pack，以获得更好的对齐
        ctk.CTkLabel(input_frame, text="输入路径:", width=80).grid(row=0, column=0, padx=5, pady=10)
        self.input_path = ctk.CTkEntry(input_frame, placeholder_text="选择需要反编译的文件或目录")
        self.input_path.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # 去掉按钮组边框，直接放置按钮
        ctk.CTkButton(
            input_frame, 
            text="浏览文件",
            width=110,
            height=35,
            font=("Microsoft YaHei UI", 12),
            command=lambda: self.browse_input(False)
        ).grid(row=0, column=2, padx=5)
        
        ctk.CTkButton(
            input_frame,
            text="浏览目录",
            width=110,
            height=35,
            font=("Microsoft YaHei UI", 12),
            command=lambda: self.browse_input(True)
        ).grid(row=0, column=3, padx=5)
        
        input_frame.grid_columnconfigure(1, weight=1)

        # 输出设置框
        output_frame = ctk.CTkFrame(self.main_frame)
        output_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(output_frame, text="输出路径:", width=80).grid(row=0, column=0, padx=5, pady=10)
        self.output_path = ctk.CTkEntry(output_frame, placeholder_text="选择输出目录")
        self.output_path.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # 去掉按钮组边框，直接放置按钮
        ctk.CTkButton(
            output_frame,
            text="浏览",
            width=110,
            height=35,
            font=("Microsoft YaHei UI", 12),
            command=self.browse_output
        ).grid(row=0, column=2, padx=5)
        
        ctk.CTkButton(
            output_frame,
            text="打开",
            width=110,
            height=35,
            font=("Microsoft YaHei UI", 12),
            command=self.open_output_dir
        ).grid(row=0, column=3, padx=5)
        
        output_frame.grid_columnconfigure(1, weight=1)

        # 操作按钮
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=25)
        
        ctk.CTkButton(
            button_frame,
            text="反编译单个文件",
            width=200,
            height=50,
            font=("Microsoft YaHei UI", 14, "bold"),
            command=lambda: self.decompile(False)
        ).pack(side="left", padx=25, pady=25)
        
        ctk.CTkButton(
            button_frame,
            text="反编译整个目录",
            width=200,
            height=50,
            font=("Microsoft YaHei UI", 14, "bold"),
            command=lambda: self.decompile(True)
        ).pack(side="left", padx=25, pady=25)

        # 日志框
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.status_text = ctk.CTkTextbox(log_frame, wrap="word")
        self.status_text.pack(fill="both", expand=True, padx=5, pady=5)

        # 初始化pycdc
        self.pycdc_path = self.extract_pycdc()

    def extract_pycdc(self):
        """从打包的程序中提取 pycdc.exe 到临时目录"""
        try:
            import tempfile
            import atexit
            import sys
            
            # 创建临时目录
            temp_dir = tempfile.mkdtemp()
            pycdc_temp_path = os.path.join(temp_dir, 'pycdc.exe')
            
            # 注册程序退出时清理临时文件
            atexit.register(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
            
            if getattr(sys, 'frozen', False):
                # 如果是包后的exe，从资源中提取pycdc.exe
                if hasattr(sys, '_MEIPASS'):
                    # PyInstaller 打包环境
                    bundled_pycdc = os.path.join(sys._MEIPASS, 'pycdc.exe')
                    if os.path.exists(bundled_pycdc):
                        shutil.copy2(bundled_pycdc, pycdc_temp_path)
                        return pycdc_temp_path
                    else:
                        self.log_message(f"错误: 在打包文件中未找到 pycdc.exe")
                        return None
            
            # 如果是开发环境，使用相对路径
            dev_pycdc = os.path.join("Release", "pycdc.exe")
            if os.path.exists(dev_pycdc):
                return dev_pycdc
            else:
                self.log_message(f"错误: 在开发环境中未找到 pycdc.exe")
                return None
            
        except Exception as e:
            self.log_message(f"提取pycdc.exe时出错: {str(e)}")
            self.log_message(f"当前路径: {os.getcwd()}")
            self.log_message(f"系统路径: {sys.path if 'sys' in locals() else '无法获取'}")
            return None

    def browse_input(self, is_dir):
        try:
            if is_dir:
                filename = filedialog.askdirectory(
                    title="选择需要反编译的目录",
                    initialdir=os.path.dirname(self.input_path.get()) if self.input_path.get() else None
                )
            else:
                filename = filedialog.askopenfilename(
                    title="选择需要反编译的文件",
                    filetypes=[("Python编译文件", "*.pyc"), ("所有文件", "*.*")],
                    initialdir=os.path.dirname(self.input_path.get()) if self.input_path.get() else None
                )
            
            if filename:
                self.input_path.delete(0, ctk.END)
                self.input_path.insert(0, filename)
                
        except Exception as e:
            self.log_message(f"选择文件时出错: {str(e)}")

    def browse_output(self):
        try:
            filename = filedialog.askdirectory(
                title="选择输出目录",
                initialdir=os.path.dirname(self.output_path.get()) if self.output_path.get() else None
            )
            if filename:
                self.output_path.delete(0, ctk.END)
                self.output_path.insert(0, filename)
                
        except Exception as e:
            self.log_message(f"选择输出目录时出错: {str(e)}")

    def log_message(self, message):
        self.status_text.insert(ctk.END, message + "\n")
        self.status_text.see(ctk.END)
        self.root.update()

    def copy_non_pyc_files(self, src_dir, dst_dir):
        """复制所有非pyc文件到目标目录"""
        try:
            copied_count = 0
            for root, _, files in os.walk(src_dir):
                for file in files:
                    if not file.endswith('.pyc'):
                        rel_path = os.path.relpath(root, src_dir)
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(dst_dir, rel_path, file)
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        copied_count += 1
            
            self.log_message(f"复制了 {copied_count} 个非pyc文件")
        
        except Exception as e:
            self.log_message(f"复制文件时出错: {str(e)}")

    def analyze_decompile_error(self, result_output, result_error):
        """分析反编译失败的原因"""
        error_info = []
        
        # 分析stderr中的错误信息
        if result_error:
            error_lines = result_error.split('\n')
            for line in error_lines:
                if 'Error' in line or 'error' in line or 'Exception' in line:
                    error_info.append(f"编译器错误: {line.strip()}")
        
        # 分析stdout中的错误标记
        if result_output:
            lines = result_output.split('\n')
            current_function = None
            error_context = []
            
            for line in lines:
                # 检测函数定义
                if line.strip().startswith('def '):
                    current_function = line.split('(')[0].replace('def ', '').strip()
                    error_context = []
                
                # 收集上下文
                error_context.append(line)
                if len(error_context) > 5:  # 持最近5行的下文
                    error_context.pop(0)
                
                # 检测各种可能的错误模式
                if '# Error' in line or '# error' in line:
                    if current_function:
                        error_info.append(f"函数 '{current_function}' 反编译失败")
                        error_info.append(f"错误代码: {line.strip()}")
                        error_info.append("上下文:")
                        error_info.extend([f"  {ctx.strip()}" for ctx in error_context])
                
                elif 'Unsupported opcode' in line:
                    error_info.append(f"不支持的字节码: {line.strip()}")
                    if current_function:
                        error_info.append(f"出现在函数: {current_function}")
                
                elif 'Invalid bytecode' in line:
                    error_info.append(f"无效的字节码: {line.strip()}")
                    if current_function:
                        error_info.append(f"出现在函数: {current_function}")
                
                elif 'Unknown magic number' in line:
                    error_info.append("Python版本不匹配: 字节码版本与反编译器不兼容")
        
        # 如果没有找到具体错误，添加通用错误信息
        if not error_info:
            error_info.append("未知错误: 无法确定具体失败原因")
            error_info.append("可能的原因:")
            error_info.append("1. 文件可能已损坏")
            error_info.append("2. Python版本不兼容")
            error_info.append("3. 使用了特殊的编译选项")
            error_info.append("4. 文件可能被加密或混淆")
        
        return error_info

    def decompile_file(self, input_file, output_file, pycdc_path, max_retries=3):
        """反编译单个文件"""
        for attempt in range(max_retries):
            try:
                # 使用 CREATE_NO_WINDOW 标志
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
                result = subprocess.run(
                    [pycdc_path, input_file], 
                    capture_output=True, 
                    text=True,
                    encoding='utf-8',
                    startupinfo=startupinfo  # 添加这个参数
                )
                
                if result.returncode == 0:
                    # 确保输出目录存在
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    
                    # 写入反编译结果
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result.stdout)
                    
                    # 检查是否有错误标记
                    if '# Error' in result.stdout or '# error' in result.stdout:
                        if attempt < max_retries - 1:
                            continue
                        return False
                    return True
                else:
                    if attempt < max_retries - 1:
                        continue
                    return False
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                self.log_message(f"错误: {str(e)}")
                return False
        
        return False

    def decompile(self, is_dir):
        input_path = self.input_path.get()
        output_dir = self.output_path.get()

        if not input_path or not output_dir:
            self.log_message("错: 请选择输入和输出路径")
            return

        # 检查pycdc.exe是否可用
        if not self.pycdc_path or not os.path.exists(self.pycdc_path):
            self.log_message("错误: pycdc.exe 不可用")
            return

        try:
            # 使用提取的pycdc.exe路径
            pycdc_path = self.pycdc_path
            
            # 检查输入类型
            if not is_dir:
                # 如果是单个文件模式
                if not os.path.isfile(input_path):
                    self.log_message("错误: 请选择一个文件而不是目录")
                    return
                    
                file_ext = os.path.splitext(input_path)[1].lower()
                if file_ext == '.py':
                    self.log_message("提示: 选择的是.py文件，无需反编译")
                    return
                elif file_ext != '.pyc':
                    self.log_message("错误: 请选择.pyc文件进行反编译，或切换到目录模式")
                    return
            else:
                # 如果是目录模式，检查是否存在pyc文件
                has_pyc = False
                for root, _, files in os.walk(input_path):
                    if any(file.endswith('.pyc') for file in files):
                        has_pyc = True
                        break
                
                if not has_pyc:
                    self.log_message("提示: 所选目录中没有找到.pyc文件")
                    return

            self.status_text.delete(1.0, ctk.END)
            self.log_message("开始处理...")
            self.log_message(f"输入路径: {input_path}")
            self.log_message(f"输出路径: {output_dir}")
            self.log_message("------------------------")

            if is_dir:
                # 首先复制非pyc文件
                self.log_message("正在复制非pyc文件...")
                self.copy_non_pyc_files(input_path, output_dir)
                
                # 统计pyc文件
                pyc_files = []
                for root, _, files in os.walk(input_path):
                    for file in files:
                        if file.endswith('.pyc'):
                            pyc_files.append((root, file))
                
                if not pyc_files:
                    self.log_message("未找到pyc文件")
                    return
                
                self.log_message(f"\n开始反编译 {len(pyc_files)} 个pyc文件...")
                
                # 处理所有pyc文件
                success_files = []
                fail_files = []
                
                for idx, (root, file) in enumerate(pyc_files, 1):
                    input_file = os.path.join(root, file)
                    rel_path = os.path.relpath(root, input_path)
                    output_file = os.path.join(
                        output_dir,
                        rel_path,
                        os.path.splitext(file)[0] + '.py'
                    )
                    
                    self.log_message(f"\n[{idx}/{len(pyc_files)}] {file}")
                    if self.decompile_file(input_file, output_file, pycdc_path):
                        success_files.append(file)
                        self.log_message(f"✓ 成功")
                    else:
                        fail_files.append(input_file)
                        self.log_message(f"✗ 失败")

                # 输出总结
                self.log_message("\n------------------------")
                self.log_message("反编译完成")
                self.log_message(f"总文件数: {len(pyc_files)}")
                self.log_message(f"成功: {len(success_files)} 个文件")
                self.log_message(f"失败: {len(fail_files)} 个文件")
                
                if fail_files:
                    self.log_message("\n失败的文件:")
                    for file in fail_files:
                        self.log_message(f"- {file}")
            else:
                # 处理单个文件
                self.log_message("开始反编译单个文件...")
                output_file = os.path.join(
                    output_dir,
                    os.path.splitext(os.path.basename(input_path))[0] + '.py'
                )
                
                if self.decompile_file(input_path, output_file, pycdc_path):
                    self.log_message("------------------------")
                    self.log_message("反编译成功！")
                    self.log_message(f"输出文件: {output_file}")
                else:
                    self.log_message("------------------------")
                    self.log_message("反编译失败！")
                    self.log_message(f"失败的文件: {input_path}")
            
        except Exception as e:
            self.log_message("------------------------")
            self.log_message(f"发生错误: {str(e)}")
            self.log_message(f"pycdc路径: {pycdc_path}")
            self.log_message(f"当前程序路径: {self.application_path}")

    def open_output_dir(self):
        output_dir = self.output_path.get()
        if not output_dir:
            self.log_message("错误: 请先选择输出路径")
            return
        
        if not os.path.exists(output_dir):
            self.log_message("错误: 输出路径不存在")
            return
        
        try:
            os.startfile(output_dir)  # Windows系统
        except AttributeError:
            try:
                subprocess.run(['xdg-open', output_dir])  # Linux系统
            except:
                try:
                    subprocess.run(['open', output_dir])  # MacOS系统
                except:
                    self.log_message("错误: 无法打开输出目录")

if __name__ == "__main__":
    try:
        # 关闭已存在的窗口
        SingletonGUI.close_existing_window()
        
        # 等待一小段时间确保旧窗口完全关闭
        time.sleep(0.1)
        
        # 创建新窗口
        root = ctk.CTk()
        app = DecompilerGUI(root)
        
        # 捕获未处理的异常并输出到日志窗口
        def handle_exception(exc_type, exc_value, exc_traceback):
            import traceback
            exception_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            app.log_message("程序发生错误:")
            app.log_message(exception_details)
        
        # 设置异常处理器
        sys.excepthook = handle_exception
        
        root.mainloop()
    except Exception as e:
        # 如果在创建窗口之前发生错误，则创建一个临时窗口显示错误
        error_root = ctk.CTk()
        error_root.withdraw()  # 隐藏主窗口
        messagebox.showerror("启动错误", str(e))
        error_root.destroy()