import wx
import json
import os

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="游戏图鉴查看器", size=(600, 400))
        self.panel = wx.Panel(self)
        icon = wx.Icon("res/icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        # 初始化数据
        self.data = self.load_data()
        self.current_dict = self.data
        self.stack = []
        
        # 创建控件
        self.list_box = wx.ListBox(self.panel, style=wx.LB_SINGLE)
        self.view_btn = wx.Button(self.panel, label="查看")
        self.back_btn = wx.Button(self.panel, label="返回")
        
        # 布局设置
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.list_box, 1, wx.EXPAND | wx.ALL, 5)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.view_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.back_btn, 0, wx.ALL, 5)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        
        self.panel.SetSizer(main_sizer)
        
        # 事件绑定
        self.list_box.Bind(wx.EVT_LISTBOX, self.on_select)
        self.view_btn.Bind(wx.EVT_BUTTON, self.on_view)
        self.back_btn.Bind(wx.EVT_BUTTON, self.on_back)
        
        # 状态栏
        self.CreateStatusBar()
        
        # 初始化显示
        self.refresh_list()

    def load_data(self):
        """加载图鉴数据"""
        if not os.path.exists("dex.json"):
            wx.MessageBox("找不到dex.json文件！", "错误", wx.OK | wx.ICON_ERROR)
            self.Destroy()
            return {}
        
        with open("dex.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def refresh_list(self):
        """刷新列表显示"""
        self.list_box.Clear()
        if self.current_dict:
            self.list_box.AppendItems(sorted(self.current_dict.keys()))
        self.UpdateWindowUI()

    def on_select(self, event):
        """列表项选择事件"""
        index = event.GetSelection()
        if index == wx.NOT_FOUND:
            self.SetStatusText("")
            return
        
        key = self.list_box.GetString(index)
        value = self.current_dict.get(key, "")
        
        if isinstance(value, dict):
            self.SetStatusText("图鉴集")
        else:
            self.SetStatusText("图鉴项")

    def on_view(self, event):
        """查看按钮事件"""
        index = self.list_box.GetSelection()
        if index == wx.NOT_FOUND:
            return
        
        key = self.list_box.GetString(index)
        value = self.current_dict.get(key, "")
        
        if isinstance(value, dict):
            self.stack.append(self.current_dict)
            self.current_dict = value
            self.refresh_list()
        else:
            self.show_content_dialog(key, value)

    def show_content_dialog(self, title, content):
        """显示内容对话框"""
        dlg = wx.Dialog(self, title=title, size=(400, 300))
        
        text = wx.TextCtrl(dlg, value=content, 
                          style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_AUTO_URL)
        text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 1, wx.EXPAND | wx.ALL, 5)
        dlg.SetSizer(sizer)
        
        dlg.ShowModal()
        dlg.Destroy()

    def on_back(self, event):
        """返回按钮事件"""
        if self.stack:
            self.current_dict = self.stack.pop()
            self.refresh_list()

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()