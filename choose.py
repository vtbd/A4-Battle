import wx
import json
import random
from typing import Iterable

def merge_dicts(dicts:Iterable[dict]) -> dict:
    merged_dict = {}
    for d in dicts:
        merged_dict = merged_dict | d
    return merged_dict
    
class GameConfigApp(wx.Frame):
    def __init__(self, parent, title):
        # 设置窗口样式，禁止调整大小
        super().__init__(parent, title=title, size=(600, 380), style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        
        # 读取角色和装备数据
        icon = wx.Icon("res/icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.names = self.load_data("names.json")
        self.settings = self.load_data("settings.json")
        self.chars_display = merge_dicts(map(lambda n: self.names[n], self.settings["display_char_keys"]))
        self.chars = self.chars_display
        self.equipment_display = merge_dicts(map(lambda n: self.names[n], self.settings["display_equipment_keys"]))
        self.equipment = self.equipment_display
        self.chars_reversed = {v : k for k,  v in self.chars.items()}
        self.equipment_reversed = {v : k for k,  v in self.equipment.items()}
        self.data = self.load_data('initialize.json')
        self.char_data = self.data['chars']
        self.equipment_data = self.data['equipment']

        # 初始场景数据
        self.scenes_display = self.names["scenes"]
        self.scenes_reversed = {v : k for k, v in self.scenes_display.items()}
        # 从 initialize.json 读取场景初始值
        self.scene_data = self.data.get("scene", "0")

        # 初始化界面
        self.init_ui()
        self.Centre()
        self.Show()

    
    def load_data(self, filename):
        """从 JSON 文件中加载数据"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            wx.MessageBox(f"文件 {filename} 未找到！", "错误", wx.ICON_ERROR)
            return {"chars": {}, "equipment": {}}

    def init_ui(self):
        """初始化界面"""
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        self.config = []  # 保存配置
        self.dropdowns = []  # 保存所有下拉框
        

        char_parameters = lambda x:{"parent": panel, "choices": list(self.chars_display.values()), "style": wx.CB_READONLY, "value": self.chars[self.char_data[x]]}
        equipment_parameters = lambda x:{"parent": panel, "choices": list(self.equipment_display.values()), "style": wx.CB_READONLY, "value": self.equipment[self.equipment_data[x]]}
        # 第一部分：前三行
        grid_sizer_top = wx.GridSizer(3, 3, 10, 10)
        for i in range(0, 3):  # 角色1到角色3
            # 角色下拉框
            char_dropdown = wx.ComboBox(**char_parameters(i))
            grid_sizer_top.Add(char_dropdown, 0, wx.EXPAND)
            self.dropdowns.append(char_dropdown)
            
            # 装备1下拉框
            equip1 = wx.ComboBox(**equipment_parameters(i*2))
            grid_sizer_top.Add(equip1, 0, wx.EXPAND)
            self.dropdowns.append(equip1)
            
            # 装备2下拉框
            equip2 = wx.ComboBox(**equipment_parameters(i*2+1))
            grid_sizer_top.Add(equip2, 0, wx.EXPAND)
            self.dropdowns.append(equip2)
            
            # 保存角色和装备的配置
            self.config.append([char_dropdown, equip1, equip2])
        
        main_sizer.Add(grid_sizer_top, 0, wx.ALL | wx.EXPAND, 15)
        
        # 添加分界线
        divider = wx.StaticLine(panel, style=wx.LI_HORIZONTAL)
        main_sizer.Add(divider, 0, wx.EXPAND | wx.ALL, 10)
        
        # 第二部分：后三行
        grid_sizer_bottom = wx.GridSizer(3, 3, 10, 10)
        for i in range(3, 6):  # 角色4到角色6
            # 角色下拉框
            char_dropdown = wx.ComboBox(**char_parameters(i))
            grid_sizer_bottom.Add(char_dropdown, 0, wx.EXPAND)
            self.dropdowns.append(char_dropdown)
            
            # 装备1下拉框
            equip1 = wx.ComboBox(**equipment_parameters(i*2))
            grid_sizer_bottom.Add(equip1, 0, wx.EXPAND)
            self.dropdowns.append(equip1)
            
            # 装备2下拉框
            equip2 = wx.ComboBox(**equipment_parameters(i*2+1))
            grid_sizer_bottom.Add(equip2, 0, wx.EXPAND)
            self.dropdowns.append(equip2)
            
            # 保存角色和装备的配置
            self.config.append([char_dropdown, equip1, equip2])
        
        main_sizer.Add(grid_sizer_bottom, 0, wx.ALL | wx.EXPAND, 15)

        # 场景布局
        scene_sizer = wx.BoxSizer(wx.HORIZONTAL)
        scene_label = wx.StaticText(panel, label="初始场景:")
        scene_sizer.Add(scene_label, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        
        # 场景下拉框
        self.scene_dropdown = wx.ComboBox(
            parent=panel,
            choices=list(self.scenes_display.values()),
            style=wx.CB_READONLY,
            value=self.scenes_display.get(self.scene_data, "默认场景")
        )
        scene_sizer.Add(self.scene_dropdown, 1, wx.EXPAND)
        
        # 将场景选择添加到主布局
        main_sizer.Add(scene_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 添加随机按钮
        random_button = wx.Button(panel, label="随机")
        random_button.Bind(wx.EVT_BUTTON, self.randomize_config)
        button_sizer.Add(random_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        # 添加保存按钮
        save_button = wx.Button(panel, label="保存配置")
        save_button.Bind(wx.EVT_BUTTON, self.save_config)
        button_sizer.Add(save_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        
        main_sizer.Add(button_sizer, 0, wx.EXPAND, 0)
        panel.SetSizer(main_sizer)

    def randomize_config(self, event):
        """随机分配角色和装备"""
        try:
            # 随机分配角色
            available_chars = list(self.chars_display.values())
            random.shuffle(available_chars)
            
            # 随机分配装备
            available_equipment_1 = list(self.equipment_display.values())
            available_equipment_2 = available_equipment_1.copy()
            random.shuffle(available_equipment_1)
            random.shuffle(available_equipment_2)
            available_equipment_both = [available_equipment_1, available_equipment_2]
            
            for i, dropdowns in enumerate(self.config):
                # 分配角色
                dropdowns[0].SetValue(available_chars.pop(0))
                
                # 分配装备（每方装备不重复）
                dropdowns[1].SetValue(available_equipment_both[i//3].pop(0))
                dropdowns[2].SetValue(available_equipment_both[i//3].pop(0))
            
            #wx.MessageBox("随机配置已完成！", "成功", wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"随机配置失败：{e}", "错误", wx.ICON_ERROR)

    def save_config(self, event):
        """保存配置到文件"""
        try:
            chars = []
            equipment = []
            for dropdowns in self.config:
                chars.append(self.chars_reversed[dropdowns[0].GetValue()])
                equipment.append(self.equipment_reversed[dropdowns[1].GetValue()])
                equipment.append(self.equipment_reversed[dropdowns[2].GetValue()])

            scene_id = self.scenes_reversed[self.scene_dropdown.GetValue()]
            out = json.dumps({
                "chars": chars,
                "equipment": equipment,
                "scene": scene_id
            })

            with open("initialize.json", "w", encoding="utf-8") as file:
                file.write(out)
                wx.MessageBox("配置已保存到 initialize.json", "成功", wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"保存失败：{e}", "错误", wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App()
    GameConfigApp(None, title="角色与装备配置")
    app.MainLoop()

