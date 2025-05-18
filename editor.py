import wx
import json
from ed_constants import *
from typing import Callable, Type
from functools import partial


def dump_json_to_file(data, f, ensure_ascii=False, indent=4, **kwargs):
    json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent, **kwargs)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="游戏配置编辑器", size=(600, 450))
        
        self.init_data()
        self.init_ui()
        self.init_menu()

        self.update_list()

    def init_data(self):
        '''初始化数据'''
        self.chars = {}
        self.equips = {}
        self.current_type = "角色"

    def init_ui(self):
        '''初始化界面'''
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 类型选择下拉框
        self.type_choice = wx.Choice(panel, choices=["角色", "装备"])
        self.type_choice.SetSelection(0)
        self.type_choice.Bind(wx.EVT_CHOICE, self.on_type_change)
        vbox.Add(self.type_choice, 0, wx.EXPAND|wx.ALL, 5)

        # 列表控件
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, "标识符", width=300)
        self.list_ctrl.InsertColumn(1, "名称", width=200)
        vbox.Add(self.list_ctrl, 1, wx.EXPAND|wx.ALL, 5)

        # 按钮面板
        btn_panel = wx.Panel(panel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_export = wx.Button(btn_panel, label="导出")
        self.btn_edit = wx.Button(btn_panel, label="编辑...")
        self.btn_delete = wx.Button(btn_panel, label="删除")
        self.btn_refresh = wx.Button(btn_panel, label="刷新")
        
        self.btn_export.Bind(wx.EVT_BUTTON, self.on_export)
        self.btn_edit.Bind(wx.EVT_BUTTON, self.on_edit)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        self.btn_refresh.Bind(wx.EVT_BUTTON, self.update_list)

        hbox.Add(self.btn_refresh, 0, wx.RIGHT, 5)
        hbox.Add(self.btn_edit, 0, wx.RIGHT, 5)
        hbox.Add(self.btn_export, 0, wx.RIGHT, 5)
        hbox.Add(self.btn_delete, 0)
        btn_panel.SetSizer(hbox)
        
        vbox.Add(btn_panel, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        # 最终设置
        panel.SetSizer(vbox)

        self.update_list()

    def init_menu(self):
        '''创建菜单栏'''
        menubar = wx.MenuBar()

        # 文件菜单
        file_menu = wx.Menu()
        save_item =file_menu.Append(wx.ID_SAVE, "保存项目\tCtrl+S")
        export_item = file_menu.Append(wx.ID_ANY, "导出")
        file_menu.AppendSeparator()
        open_item = file_menu.Append(wx.ID_OPEN, "打开项目\tCtrl+O")
        import_item = file_menu.Append(wx.ID_ANY, "导入")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "退出\tCtrl+Q")
        menubar.Append(file_menu, "文件")
        
        # 编辑菜单
        edit_menu = wx.Menu()
        new_char_item = edit_menu.Append(wx.ID_NEW, "新建角色")
        new_equip_item = edit_menu.Append(wx.ID_ADD, "新建装备")
        menubar.Append(edit_menu, "编辑")
        
        # 帮助菜单
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "关于")
        menubar.Append(help_menu, "帮助")
        
        self.SetMenuBar(menubar)

        # 绑定菜单事件
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_export, export_item)
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_import, import_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_new_char, new_char_item)
        self.Bind(wx.EVT_MENU, self.on_new_equip, new_equip_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    def on_type_change(self, event):
        """切换显示类型"""
        self.current_type = self.type_choice.GetStringSelection()
        self.update_list()

    def on_save(self, event):
        """保存整个项目"""
        data = {
            "chars": self.chars,
            "equips": self.equips
        }
        
        with wx.FileDialog(self, "保存项目", wildcard="A4 Battle 项目文件 (*.a4b)|*.a4b",
                          style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
            with open(path, 'w', encoding='utf-8') as f:
                dump_json_to_file(data, f)

    def on_export(self, event):
        """导出所选项目"""
        selected_count = self.list_ctrl.GetSelectedItemCount()
        if selected_count == 0:
            wx.MessageBox("请先选择一个项目！", "提示", wx.OK|wx.ICON_INFORMATION)
            return
        selected = self.selected_item_first
        if selected_count > 1:
            wx.MessageBox(f"目前暂时只支持导出单个项目。将导出首个项目：{selected}", "提示", wx.OK|wx.ICON_INFORMATION)
        
        data = self.current_data.get(selected)
        if not data:
            wx.MessageBox("项目已不存在，请刷新", "提示", wx.OK|wx.ICON_INFORMATION)
            return
        
        # 保存文件对话框
        with wx.FileDialog(self, "导出文件", wildcard="JSON文件 (*.json)|*.json",
                          style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
            with open(path, 'w', encoding='utf-8') as f:
                dump_json_to_file(data, f)
            
    def on_open(self, event):
        """打开项目文件"""
        with wx.FileDialog(self, "打开项目", wildcard="A4 Battle (*.a4b)|*.a4b|所有文件|*.*",
                          style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if self.project_validator(data):
                        self.chars = data.get("chars", {})
                        self.equips = data.get("equips", {})
                        self.update_list()
                    else:
                        raise ValueError
                except:
                    wx.MessageBox(f"{path} 不是合法的项目文件", "错误", wx.OK|wx.ICON_ERROR)
                    return

    def on_import(self, event): 
        wx.MessageBox("暂未开放", "提示", wx.OK|wx.ICON_INFORMATION)
                    
    def on_exit(self, event):
        with wx.MessageDialog(
            parent=self,
            message="是否确认退出？",
            caption="退出",
            style=wx.YES_NO|wx.ICON_QUESTION
        ) as dlg:
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()

    def on_about(self, event):
        wx.MessageBox("A4 Battle 游戏配置编辑器\n软件由橙子制作", "关于", wx.OK|wx.ICON_INFORMATION)

    def on_new_char(self, event):
        editor = CharEditor(self)
        editor.ShowModal()
        if editor.confirmed:
            self.save_char_from_editor(editor)

    def on_new_equip(self, event):
        pass

    def on_edit(self, event):
        selected = self.selected_items
        if len(selected) == 0:
            return
        if len(selected) > 1:
            return
        
        data:dict = self.current_data.get(selected[0], {})
        
        if self.current_type == "角色":
            editor = CharEditor(self, data.copy())
            editor.ShowModal()
            if editor.confirmed:
                self.save_char_from_editor(editor)
                
        elif self.current_type == "装备":
            # 装备编辑逻辑（待实现）
            pass

    def on_delete(self, event):
        """删除所选项目"""
        selected = self.selected_items
        
        if len(selected) == 0:
            return
        if len(selected) == 1:
            confirm_text = f"确定要删除 '{selected[0]}' 吗？"
        else:
            confirm_text = f"确定要删除 {len(selected)} 个项目吗？"

        confirm = wx.MessageBox(confirm_text, 
                            "确认删除", wx.YES_NO|wx.ICON_WARNING)
        if confirm == wx.YES:
            data_dict = self.current_data
            for item in selected:
                del data_dict[item]
            self.update_list()

    def update_list(self, event=None):
        """更新列表显示"""
        self.list_ctrl.DeleteAllItems()
        data_dict = self.current_data
        
        for idx, (identifier, data) in enumerate(data_dict.items()):
            self.list_ctrl.InsertItem(idx, identifier)
            self.list_ctrl.SetItem(idx, 1, data.get("name", ""))

    def save_char_from_editor(self, editor):
        identifier = editor.get_identifier()
        if identifier:
            self.chars[identifier] = editor.data
            self.update_list()

    def project_validator(self, project):
        """检测项目是否合法"""
        if type(project) != dict:
            return False
        else:
            chars = project.get("chars")
            if type(chars) != dict:
                return False
            else:
                for char in chars.values():
                    if self.char_validator(char) == False:
                        return False
            equips = project.get("equips")
            if type(equips) != dict:
                return False
            else:
                for equip in equips.values():
                    if self.equip_validator(equip) == False:
                        return False
        return True

    def char_validator(self, char):
        return True

    def equip_validator(self, equip):
        return True

    @property
    def current_data(self):
        """获取当前显示的数据"""
        return self.chars if self.current_type == "角色" else self.equips

    @property
    def selected_item_first(self):
        """获取选中的第一个项目标识符"""
        selected = self.list_ctrl.GetFirstSelected()
        if selected == -1:
            return None
        return self.list_ctrl.GetItemText(selected)
    
    @property
    def selected_items(self):
        """获取选中的所有项目标识符"""
        items = []
        selected = self.list_ctrl.GetFirstSelected()
        while selected != -1:
            items.append(selected)
            selected = self.list_ctrl.GetNextSelected(selected)
        return list(map(self.list_ctrl.GetItemText, items))
    
class BaseEditorWindow(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self._init_ui()
        self.confirmed = False

    def _init_ui(self):
        """ui 初始化"""
        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 滚动区域配置
        self.scroll = wx.ScrolledWindow(self.main_panel)
        self.form_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll.SetSizer(self.form_sizer)
        self.scroll.SetScrollRate(20, 20)
        self.scroll.SetMinSize((-1, 400))  # 最小高度
        self.main_sizer.Add(self.scroll, 1, wx.EXPAND|wx.ALL, 5)

        self.main_panel.SetSizer(self.main_sizer)

    def _init_bottom_zone(
            self, 
            label_text="标识符:", 
            save_func:Callable[[int|None, wx.Dialog], None]=None, 
            cancel_func:Callable[[int|None, wx.Dialog], None]=None):
        '''底部输入区域配置。`save_func` 和 `cancel_func` 分别在点击保存和取消按钮时被调用，他们接受一个 `event` 参数和一个指示自身的 `dialog_self` 参数，没有返回值。注意一定要在该函数中关闭窗口。'''
        
        if save_func == None:
            save_func = BaseEditorWindow.default_save_func
            
        if cancel_func == None:
            cancel_func = BaseEditorWindow.default_cancel_func

        self.id_panel = wx.Panel(self.main_panel)

        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_identifier = wx.StaticText(self.id_panel, label=label_text)
        bottom_sizer.Add(self.lbl_identifier, 0, wx.ALIGN_CENTER|wx.RIGHT, 5)

        self.txt_bottom = wx.TextCtrl(self.id_panel)
        bottom_sizer.Add(self.txt_bottom, 1, wx.EXPAND|wx.RIGHT, 10)

        self.btn_save = wx.Button(self.id_panel, label="保存并返回")
        self.btn_save.Bind(wx.EVT_BUTTON, lambda e:save_func(e, self))
        bottom_sizer.Add(self.btn_save, 0, wx.RIGHT, 5)

        self.btn_cancel = wx.Button(self.id_panel, label="取消")
        self.btn_cancel.Bind(wx.EVT_BUTTON, lambda e:cancel_func(e, self))
        bottom_sizer.Add(self.btn_cancel, 0)

        self.id_panel.SetSizer(bottom_sizer)

        self.main_sizer.Add(self.id_panel, 0, wx.EXPAND|wx.ALL, 5)
    
    def add_form_row(self, label_text, control_class: Type[wx.Window], *args, **kwargs):
        """添加表单行并返回控件对象。`control_class` 参数是对应的 wx 控件类"""
        row_panel = wx.Panel(self.scroll)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lbl = wx.StaticText(row_panel, label=label_text)
        control = control_class(row_panel, *args, **kwargs)
        
        sizer.Add(lbl, 0, wx.ALIGN_CENTER|wx.RIGHT, 10)
        sizer.Add(control, 1, wx.EXPAND)
        row_panel.SetSizer(sizer)
        self.form_sizer.Add(row_panel, 0, wx.EXPAND|wx.ALL, 5)
        return control
    
    def add_label(self, label_text):
        """添加一行静态文本"""
        lbl = wx.StaticText(self.scroll, label=label_text)
        
        self.form_sizer.Add(lbl, 0, wx.ALIGN_LEFT|wx.ALL, 10)
    
    def add_custom_control(self, panel_builder: Callable[[wx.Window], wx.Panel]):
        """添加自定义控件组。`panel_builder` 参数是一个接受一个参数 `parent` 作为所添加控件的父控件，返回 `wx.Panel` 类的实例作为添加的控件的函数。"""
        custom_panel = panel_builder(self.scroll)
        self.form_sizer.Add(custom_panel, 0, wx.EXPAND|wx.ALL, 5)

    def add_custom_control_line(self, label_text, panel_builder: Callable[[wx.Window], wx.Panel]):
        """添加单行，左侧为标签，右侧为自定义控件组。`panel_builder` 参数是一个接受一个参数 `parent` 作为所添加控件的父控件，返回 `wx.Panel` 类的实例作为添加的控件的函数。"""
        row_panel = wx.Panel(self.scroll)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lbl = wx.StaticText(row_panel, label=label_text)
        custum_panel = panel_builder(row_panel)
        
        sizer.Add(lbl, 0, wx.ALIGN_CENTER|wx.RIGHT, 10)
        sizer.Add(custum_panel, 0, wx.EXPAND)
        row_panel.SetSizer(sizer)
        self.form_sizer.Add(row_panel, 0, wx.EXPAND|wx.ALL, 5)

    def add_stretch(self):
        """添加弹性空白"""
        self.form_sizer.AddStretchSpacer()
    
    @staticmethod
    def default_save_func(event, dialog_self):
        dialog_self.confirmed = True
        dialog_self.Close()

    @staticmethod
    def default_cancel_func(event, dialog_self):
        dialog_self.confirmed = False
        dialog_self.Close()

class SkillControl(wx.Panel):
    """技能行"""
    def __init__(self, parent, index, func, **kwargs):
        super().__init__(parent, **kwargs)
        self.index = index
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_skill = wx.TextCtrl(self, style=wx.TE_READONLY)
        btn_edit = wx.Button(self, label="编辑...", size=(80, -1))
        btn_edit.Bind(wx.EVT_BUTTON, func)

        sizer.Add(self.txt_skill, 1, wx.EXPAND|wx.RIGHT, 5)
        sizer.Add(btn_edit, 0)
        self.SetSizer(sizer)

    def update_name(self, data):
        self.txt_skill.SetValue(data.get("skill", [{}, {}, {}])[self.index].get("name", ""))

class CharEditor(BaseEditorWindow):
    def __init__(self, parent, data:dict={}):
        super().__init__(parent, "角色编辑")

        self.load_data(data)
        if not data.get("skill"):
            self._init_skill_data()

        def save_func(event, dialog_self):
            idf = self.get_identifier()
            if idf == "":
                wx.MessageBox(
                    "请输入标识名！", 
                    "错误", 
                    wx.ICON_WARNING
                )
                return
            if idf in self.Parent.chars.keys():
                confirm = wx.MessageBox(f"标识符 '{idf}' 已存在。要替换它吗？", 
                                    "提示", wx.YES_NO|wx.ICON_WARNING)
                if confirm == wx.NO:
                    return
            self.update_direct_data()
            CharEditor.default_save_func(event, dialog_self)

        self._init_bottom_zone(save_func=save_func)
        
        self.txt_name:wx.TextCtrl = self.add_form_row("角色名称:", wx.TextCtrl)
        self.spn_attack:wx.SpinCtrl = self.add_form_row("攻击力:", wx.SpinCtrl, min=0, max=999)
        self.spn_health:wx.SpinCtrl = self.add_form_row("生命值:", wx.SpinCtrl, min=0, max=999)
        self.cmb_group:wx.ComboBox = self.add_form_row("组别:", wx.ComboBox, 
                                         choices=list(ED_CHAR_GROUP_READER.keys()), 
                                         style=wx.CB_READONLY)
        self.skill_controls = []
        #for i in range(3):
        #    new_btn = self.add_form_row(f"技能{i+1}:", wx.Button, label="编辑...")
        #    func = partial(self._on_edit_skill, index=i)
        #    new_btn.Bind(wx.EVT_BUTTON, func)
        #    self.skill_controls.append(new_btn)
        for i in range(3):
            func = partial(self._on_edit_skill, index=i)
            skill_control = self.add_form_row(f"技能{i+1}:", SkillControl, index=i, func=func)
            self.skill_controls.append(skill_control)

        self.set_data()
        self.add_stretch()

    def _init_skill_data(self):
        self.data["skill"] = [{}, {}, {}]

    def _on_edit_skill(self, event, index):
        """打开技能编辑器"""
        editor = SkillEditor(self, self.data["skill"][index].copy())
        editor.ShowModal()
        if editor.confirmed:
            self.save_skill_to_data(index, editor)
        self.set_skill_controls()

    def save_skill_to_data(self, index, editor):
        skill_data = editor.data.copy()
        skill_data["__skill__"] = True
        self.data["skill"][index] = skill_data

    def load_data(self, data:dict):
        """加载数据"""
        self.data = data
    
    def set_data(self, event=None):
        """将加载的数据设置个给控件"""
        self.txt_name.SetValue(self.data.get("name", ""))
        self.spn_attack.SetValue(self.data.get("attack", 0))
        self.spn_health.SetValue(self.data.get("health", 0))
        self.cmb_group.SetStringSelection(ED_CHAR_GROUP_READER_INVERT[self.data.get("group", 0)])
        self.txt_bottom.SetValue(self.data.get("__identifier__", ""))
        self.set_skill_controls()

    def set_skill_controls(self):
        for i, sc in enumerate(self.skill_controls):
            sc.update_name(self.data)

    def update_direct_data(self):
        """将在本窗口中直接编辑的数据写入 `self.data` 属性中"""
        self.data["name"] = self.txt_name.GetValue()
        self.data["attack"] = self.spn_attack.GetValue()
        self.data["health"] = self.spn_health.GetValue()
        self.data["group"] = ED_CHAR_GROUP_READER[self.cmb_group.GetStringSelection()]
        self.data["__identifier__"] = self.txt_bottom.GetValue()

    def get_identifier(self):
        return self.txt_bottom.GetValue()
    
class SkillEditor(BaseEditorWindow):
    def __init__(self, parent, data:dict = {}):
        super().__init__(parent, "技能编辑器")

        self.load_data(data)

        def save_func(event, dialog_self):
            self.update_direct_data()
            SkillEditor.default_save_func(event, dialog_self)

        self._init_bottom_zone(label_text="技能储存名（暂无效）", save_func=save_func)

        # 基础属性
        self.txt_name = self.add_form_row("技能名称:", wx.TextCtrl)
        self.txt_desc = self.add_form_row("技能描述:", wx.TextCtrl, style=wx.TE_MULTILINE)
        self.cmb_type = self.add_form_row("技能类型:", wx.ComboBox, 
                                        choices=list(ED_SKILL_TYPE_READER.keys()), 
                                        style=wx.CB_READONLY)
        
        self.add_label("效果：")
        # 效果列表区域（使用自定义控件组）
        def build_effect_panel(parent):
            panel = wx.Panel(parent)
            self.effect_list = wx.ListBox(panel, style=wx.LB_SINGLE)
            self.btn_add = wx.Button(panel, label="新建")
            self.btn_edit = wx.Button(panel, label="编辑")
            self.btn_del = wx.Button(panel, label="删除")
            
            btn_sizer = wx.BoxSizer(wx.VERTICAL)
            btn_sizer.Add(self.btn_add, 0, wx.BOTTOM, 5)
            btn_sizer.Add(self.btn_edit, 0, wx.BOTTOM, 5)
            btn_sizer.Add(self.btn_del, 0)
            
            main_sizer = wx.BoxSizer(wx.HORIZONTAL)
            main_sizer.Add(self.effect_list, 1, wx.EXPAND|wx.RIGHT, 10)
            main_sizer.Add(btn_sizer, 0)
            panel.SetSizer(main_sizer)
            return panel
        
        self.add_custom_control(build_effect_panel)
        self.add_stretch()

        # 绑定效果按钮事件
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_add_effect)
        self.btn_edit.Bind(wx.EVT_BUTTON, self.on_edit_effect)
        self.btn_del.Bind(wx.EVT_BUTTON, self.on_delete_effect)

        self.set_data()

    def on_add_effect(self, event):
        """添加新效果"""
        editor = EffectEditor(self)
        editor.ShowModal()
        if editor.confirmed:
            new_effect = editor.data
            if "effect" not in self.data:
                self.data["effect"] = []
            self.data["effect"].append(new_effect)
            self.effect_list.Append(new_effect.get("name", "未命名效果"))

    def on_edit_effect(self, event):
        """编辑选中的效果"""
        selection = self.effect_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox("请先选择一个效果！", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        effect_data = self.data["effect"][selection]
        editor = EffectEditor(self, effect_data.copy())
        editor.ShowModal()
        if editor.confirmed:
            updated_effect = editor.data
            self.data["effect"][selection] = updated_effect
            self.effect_list.SetString(selection, updated_effect.get("name", "未命名效果"))

    def on_delete_effect(self, event):
        """删除选中的效果"""
        selection = self.effect_list.GetSelection()
        if selection != wx.NOT_FOUND:
            del self.data["effect"][selection]
            self.effect_list.Delete(selection)

    def load_data(self, data:dict):
        """加载数据"""
        self.data = data

    def set_data(self):
        """将加载的数据设置个给控件"""
        self.txt_name.SetValue(self.data.get("name", ""))
        self.txt_desc.SetValue(self.data.get("description", ""))
        self.cmb_type.SetStringSelection(ED_SKILL_TYPE_READER_INVERT[self.data.get("type", 1)])
        self.effect_list:wx.ListBox
        self.update_effect_list()

    def update_direct_data(self):
        """将在本窗口中直接编辑的数据写入 `self.data` 属性中"""
        self.data["name"] = self.txt_name.GetValue()
        self.data["description"] = self.txt_desc.GetValue()
        self.data["type"] = ED_SKILL_TYPE_READER[self.cmb_type.GetStringSelection()]

    def update_effect_list(self):
        """刷新列表"""
        self.effect_list.Clear()
        self.effect_list.AppendItems(list(map(lambda x:x.get("name", "未命名效果"), self.data.get("effect", []))))

class EffectEditor(BaseEditorWindow):
    pass

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.chars = {"char1": {"name": "角色1"}, "char2": {"name": "角色2"}}
    frame.equips = {"equip1": {"name": "装备1"}, "equip2": {"name": "装备2"}}
    frame.Show()
    app.MainLoop()