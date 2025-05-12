import json
import tkinter as tk
from tkinter import ttk

class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏设置")
        self.root.iconbitmap("res/icon.ico")
        self.settings = {}
        self.setting_widgets = []
        
        # 创建样式并配置无边框Frame
        self.style = ttk.Style()
        self.style.configure('NoBorder.TFrame', borderwidth=0, relief='flat')

        # 创建滚动区域# 修改Canvas配置（添加背景色）
        self.canvas = tk.Canvas(
            root, 
            borderwidth=0,
            highlightthickness=0,  # 禁用高亮边框
            background='#f0f0f0'   # 与主窗口背景一致
        )
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        # 修改滚动区域Frame配置
        self.scrollable_frame = ttk.Frame(
            self.canvas, 
            style='NoBorder.TFrame'
        )

        # 配置滚动区域
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # 布局
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # 绑定滚动区域调整事件
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # 创建控件
        self.create_widgets()
        self.create_save_button()
        
        # 加载设置
        self.load_settings()

    def create_widgets(self):
        """创建设置控件"""
        # 窗口缩放控件
        self.size_var = tk.DoubleVar()
        size_frame = ttk.Frame(self.scrollable_frame, style='NoBorder.TFrame')
        size_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(size_frame, text="窗口缩放 (0.2-1):").pack(side="left")
        scale = ttk.Scale(
            size_frame,
            from_=0.2,
            to=1.0,
            variable=self.size_var,
            command=lambda v: self.size_label.config(text=f"{float(v):.2f}")
        )
        scale.pack(side="left", expand=True, fill="x", padx=5)
        
        self.size_label = ttk.Label(size_frame, text="1.00", width=5)
        self.size_label.pack(side="left")
        self.setting_widgets.append(("size", self.size_var))

        # 背景显示复选框
        self.bg_var = tk.BooleanVar()
        bg_frame = ttk.Frame(self.scrollable_frame, style='NoBorder.TFrame')
        bg_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Checkbutton(
            bg_frame,
            text="显示场景背景",
            variable=self.bg_var
        ).pack(anchor="w")
        self.setting_widgets.append(("show_scene_background", self.bg_var))

    def create_save_button(self):
        """创建保存按钮"""
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ttk.Button(
            btn_frame,
            text="保存设置",
            command=self.save_settings
        ).pack(side="bottom", fill="x")

    def load_settings(self):
        """从文件加载设置"""
        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
                
            for name, var in self.setting_widgets:
                if name in self.settings:
                    var.set(self.settings[name])
                    if name == "size":
                        self.size_label.config(text=f"{self.settings[name]:.2f}")

        except FileNotFoundError:
            self.settings = {"size": 1.0, "show_scene_background": True}

    def save_settings(self):
        """保存设置到文件"""
        for name, var in self.setting_widgets:
            self.settings[name] = var.get()
        
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)

    def on_frame_configure(self, event):
        """更新滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """调整canvas窗口宽度"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)


def main():
    root = tk.Tk()
    root.geometry("400x300")
    root.minsize(300, 200)
    app = SettingsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()