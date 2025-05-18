import wx
import json
from pathlib import Path

class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings_file = Path("settings.json")
        self.settings = self.load_settings()
        
        # 主Sizer (垂直布局)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 创建滚动窗口
        self.scrolled = wx.ScrolledWindow(self)
        self.scrolled.SetScrollRate(10, 10)
        
        # 滚动窗口的内容Sizer
        self.scrolled_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 创建控件
        self.create_controls()
        
        # 设置滚动窗口的Sizer
        self.scrolled.SetSizer(self.scrolled_sizer)
        
        # 添加滚动窗口到主Sizer，可扩展
        self.main_sizer.Add(self.scrolled, 1, wx.EXPAND | wx.ALL, 0)
        
        # 添加保存按钮到主Sizer，不扩展
        self.save_btn = wx.Button(self, label="保存设置")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        self.main_sizer.Add(self.save_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        self.SetSizer(self.main_sizer)
        self.Layout()
    
    def load_settings(self):
        """加载设置文件"""
        default_settings = {
            "size": 1.0,
            "show_scene_background": False,
            "display_char_keys": ["chars_normal"],
            "display_equipment_keys": ["equipment"]
        }
        
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default_settings
        except (json.JSONDecodeError, IOError):
            return default_settings
    
    def save_settings(self):
        """保存设置到文件"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except IOError:
            return False
    
    def create_controls(self):
        """在滚动窗口中创建所有设置控件"""
        
        # 窗口缩放大小
        size_box = wx.StaticBox(self.scrolled, label="窗口缩放大小")
        size_sizer = wx.StaticBoxSizer(size_box, wx.VERTICAL)
        
        self.size_slider = wx.Slider(self.scrolled, value=int(self.settings["size"] * 10), 
                                    minValue=2, maxValue=10, 
                                    style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.size_slider.Bind(wx.EVT_SLIDER, self.on_size_change)
        
        self.size_text = wx.StaticText(self.scrolled, label=f"当前值: {self.settings['size']}")
        size_sizer.Add(self.size_slider, 0, wx.EXPAND | wx.ALL, 5)
        size_sizer.Add(self.size_text, 0, wx.LEFT | wx.BOTTOM, 5)
        self.scrolled_sizer.Add(size_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # 显示场景背景
        self.bg_check = wx.CheckBox(self.scrolled, label="显示场景背景")
        self.bg_check.SetValue(self.settings["show_scene_background"])
        self.scrolled_sizer.Add(self.bg_check, 0, wx.ALL, 10)
        
        # 角色类型选择
        char_box = wx.StaticBox(self.scrolled, label="角色类型")
        char_sizer = wx.StaticBoxSizer(char_box, wx.VERTICAL)
        
        self.char_choices = {
            "chars_normal": "常规角色",
            "chars_fun": "娱乐角色",
            "chars_test": "测试角色"
        }
        
        self.char_boxes = []
        for key, label in self.char_choices.items():
            cb = wx.CheckBox(self.scrolled, label=label)
            cb.SetValue(key in self.settings["display_char_keys"])
            char_sizer.Add(cb, 0, wx.ALL, 5)
            self.char_boxes.append((key, cb))
        
        self.scrolled_sizer.Add(char_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # 装备类型选择
        equip_box = wx.StaticBox(self.scrolled, label="装备类型")
        equip_sizer = wx.StaticBoxSizer(equip_box, wx.VERTICAL)
        
        self.equip_choices = {
            "equipment": "常规装备",
            "equipment_test": "测试装备"
        }
        
        self.equip_boxes = []
        for key, label in self.equip_choices.items():
            cb = wx.CheckBox(self.scrolled, label=label)
            cb.SetValue(key in self.settings["display_equipment_keys"])
            equip_sizer.Add(cb, 0, wx.ALL, 5)
            self.equip_boxes.append((key, cb))
        
        self.scrolled_sizer.Add(equip_sizer, 0, wx.EXPAND | wx.ALL, 10)
    
    def on_size_change(self, event):
        """处理缩放大小变化"""
        value = self.size_slider.GetValue() / 10.0
        self.size_text.SetLabel(f"当前值: {value:.1f}")
        self.settings["size"] = value
    
    def on_save(self, event):
        """保存按钮事件处理"""
        # 更新设置值
        self.settings["show_scene_background"] = self.bg_check.GetValue()
        
        # 更新角色选择
        self.settings["display_char_keys"] = [
            key for key, cb in self.char_boxes if cb.GetValue()
        ]
        
        # 更新装备选择
        self.settings["display_equipment_keys"] = [
            key for key, cb in self.equip_boxes if cb.GetValue()
        ]
        
        # 保存到文件
        if self.save_settings():
            wx.MessageBox("设置保存成功！", "成功", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("保存设置失败！", "错误", wx.OK | wx.ICON_ERROR)

class SettingsFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="游戏设置", size=(400, 500))
        
        # 创建主面板
        self.panel = SettingsPanel(self)
        
        # 设置窗口最小大小
        self.SetMinSize(wx.Size(200, 200))
        
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = SettingsFrame()
    app.MainLoop()