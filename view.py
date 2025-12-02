import os
import sys
from ast import literal_eval
import ttkbootstrap as ttk
import tkinter.messagebox as messagebox
from tkinter import *
from lib import *
def get_resource_path(relative_path):
    """返回资源文件的绝对路径"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

app = ttk.Window(themename="cosmo")
app.title("莫名其妙工具箱")
app.geometry("800x600")
icon_path = get_resource_path("icon.ico")
app.iconbitmap(icon_path)

def switch_content(content_type):
    for widget in main_content.winfo_children():
        widget.destroy()
    if content_type == "进制转换-简单":
        label = ttk.Label(main_content, text="进制转换器（正整数）", font=("Arial", 16))
        label.pack(pady=20)

        label2 = ttk.Label(main_content, text="转换前的进制", font=("Arial", 12))
        label2.pack(pady=5)

        from_base1 = ttk.StringVar()
        j = [str(i) for i in range(2, 37)]
        combo1 = ttk.Combobox(main_content, values=j, state="readonly", textvariable=from_base1)
        combo1.pack(pady=5)

        label3 = ttk.Label(main_content, text="转换后的进制", font=("Arial", 12))
        label3.pack(pady=5)

        to_base1 = ttk.StringVar()
        combo2 = ttk.Combobox(main_content, values=j, state="readonly", textvariable=to_base1)
        combo2.pack(pady=5)

        label4 = ttk.Label(main_content, text="要转换的内容", font=("Arial", 12))
        label4.pack(pady=5)

        vcmd = main_content.register(validate_input)
        # 创建输入框，设置验证规则
        entry = ttk.Entry(main_content, validate="key", validatecommand=(vcmd, "%P"))
        entry.pack(pady=5)

        def convert():
            # 调用 convert_base 并获取结果
            try:
                if entry.get()=='':
                    messagebox.showerror("错误", "请输入内容")
                    return
                if not validate_input(entry.get()):
                    messagebox.showerror("错误", "请输入正确的内容")
                    return
                if from_base1.get()=='' or to_base1.get()=='':
                    messagebox.showerror("错误", "请选择进制")
                    return
                result = convert_base(entry.get(), int(from_base1.get()), int(to_base1.get()))
            except Exception as e:
                result = str(e)
                messagebox.showerror("错误", result)
                return
            text_result.config(state="normal")  # 解锁 Text 控件
            text_result.delete("1.0", "end")  # 清空当前内容
            text_result.insert("1.0", result)  # 插入转换结果
            text_result.config(state="disabled")  # 设置为只读

        btn_main1 = ttk.Button(main_content, text="转换", style="primary.TButton", command=convert)
        btn_main1.pack(pady=5)

        text_result = ttk.Text(main_content, height=3, width=30, state="disabled")
        text_result.pack(pady=5)
    elif content_type == "进制转换-高级":
        # 给右侧区域添加标签
        label = ttk.Label(main_content, text="进制转换器（包含负数和小数）", font=("Arial", 16))
        label.pack(pady=20)

        label2 = ttk.Label(main_content, text="转换前的进制", font=("Arial", 12))
        label2.pack(pady=5)

        from_base1 = ttk.StringVar()
        j = [str(i) for i in range(2, 37)]
        combo1 = ttk.Combobox(main_content, values=j, state="readonly", textvariable=from_base1)
        combo1.pack(pady=5)

        label3 = ttk.Label(main_content, text="转换后的进制", font=("Arial", 12))
        label3.pack(pady=5)

        to_base1 = ttk.StringVar()
        combo2 = ttk.Combobox(main_content, values=j, state="readonly", textvariable=to_base1)
        combo2.pack(pady=5)

        label4 = ttk.Label(main_content, text="要转换的内容", font=("Arial", 12))
        label4.pack(pady=5)

        vcmd = main_content.register(validate_input)
        # 创建输入框，设置验证规则
        entry = ttk.Entry(main_content, validate="key", validatecommand=(vcmd, "%P"))
        entry.pack(pady=5)
        def convert():
            # 调用 convert_base 并获取结果
            try:
                if entry.get()=='':
                    messagebox.showerror("错误", "请输入内容")
                    return
                if not validate_input(entry.get()):
                    messagebox.showerror("错误", "请输入正确的内容")
                    return
                if from_base1.get()=='' or to_base1.get()=='':
                    messagebox.showerror("错误", "请选择进制")
                    return
                result = convert_base(entry.get(), int(from_base1.get()), int(to_base1.get()))
            except Exception as e:
                result = str(e)
                messagebox.showerror("错误", result)
                return
            text_result.config(state="normal")  # 解锁 Text 控件
            text_result.delete("1.0", "end")  # 清空当前内容
            text_result.insert("1.0", result)  # 插入转换结果
            text_result.config(state="disabled")  # 设置为只读

        btn_main1 = ttk.Button(main_content, text="转换", style="primary.TButton", command=convert)
        btn_main1.pack(pady=5)

        text_result = ttk.Text(main_content, height=3, width=30, state="disabled")
        text_result.pack(pady=5)


sidebar = ttk.Frame(app, width=200, padding=10, relief="solid")
sidebar.grid(row=0, column=0, sticky="ns")  # 使用 grid 布局将侧边栏放在左侧

# 在侧边栏中添加按钮
btn1 = ttk.Button(sidebar, text="进制转换-简单", style="primary.TButton",command=lambda: switch_content("进制转换-简单"))
btn1.grid(row=0, column=0, pady=10, sticky="ew")

btn2 = ttk.Button(sidebar, text="进制转换-高级", style="primary.TButton",command=lambda: switch_content("进制转换-高级"))
btn2.grid(row=1, column=0, pady=10, sticky="ew")

btn3 = ttk.Button(sidebar, text="关于", style="primary.TButton")
btn3.grid(row=2, column=0, pady=10, sticky="ew")

# 创建主内容区域（右侧）
main_content = ttk.Frame(app, padding=10)
main_content.grid(row=0, column=1, sticky="nsew")  # 右侧区域占满剩余空间

# 配置 grid 布局的权重，确保右侧区域自适应大小
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# 初始化显示主页内容
switch_content("进制转换-简单")

# 运行主事件循环
app.mainloop()