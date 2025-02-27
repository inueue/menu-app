import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import json
import os
import sys
import requests
import webbrowser
from packaging import version
import tempfile
import subprocess
import zipfile
import shutil
from urllib.request import urlretrieve

# 尝试导入 winotify，如果不存在则使用备用方案
try:
    from winotify import Notification
    HAS_WINOTIFY = True
except ImportError:
    HAS_WINOTIFY = False

class MenuApp:
    VERSION = "1.0.0"  # 当前版本号

    def get_resource_path(self, relative_path):
        """获取资源文件的路径"""
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            base_path = sys._MEIPASS
        else:
            # 如果是python脚本
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def center_window(self, window):
        """使窗口在屏幕中居中"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"+{x}+{y}")

    def __init__(self, root):
        self.root = root
        self.root.title("今天吃什么 - 欣仔专用")
        
        # 设置主窗口大小
        window_width = 420
        window_height = 620
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(False, False)
        
        # 居中显示主窗口
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 设置程序图标
        icon_path = self.get_resource_path('icon.ico')
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # 初始化默认菜单
        self.default_menu = {
            "农家小炒肉": (25, "荤菜"),
            "川味回锅肉": (28, "荤菜"),
            "青椒肉丝": (25, "荤菜"),
            "台湾三杯鸡": (28, "荤菜"),
            "辣子鸡": (28, "荤菜"),
            "冬菇滑鸡": (28, "荤菜"),
            "农家一碗香": (28, "荤菜"),
            "酸辣鸡杂": (25, "荤菜"),
            "姜葱炒猪杂": (28, "荤菜"),
            "姜葱炒脆肠": (32, "荤菜"),
            "尖椒炒猪肚": (38, "荤菜"),
            "尖椒炒牛肉": (35, "荤菜"),
            "凉瓜炒牛肉": (32, "荤菜"),
            "白切鸡": (40, "荤菜"),
            "广式葱油鸡": (40, "荤菜"),
            "铁板黑椒牛肉": (38, "荤菜"),
            "水煮牛肉": (38, "荤菜"),
            "水煮肉片": (30, "荤菜"),
            "水煮鱼片": (30, "荤菜"),
            "老坛酸菜鱼": (30, "荤菜"),
            "尖椒焖鸭": (28, "荤菜"),
            "尖椒炒腊肉": (30, "荤菜"),
            "糖醋排骨": (35, "荤菜"),
            "红烧排骨": (32, "荤菜"),
            "红烧肥肠": (35, "荤菜"),
            "红烧鱼腩": (28, "荤菜"),
            "酸菜肥肠": (35, "荤菜"),
            "干煸肥肠": (35, "荤菜"),
            "干锅肥肠": (35, "荤菜"),
            "干锅鸡": (30, "荤菜"),
            "咕噜肉": (30, "荤菜"),
            "干锅土豆片": (22, "荤菜"),
            "砂锅鸡煲": (35, "荤菜"),
            "小炒拆骨肉": (28, "荤菜"),
            "小炒牛肉": (35, "荤菜"),
            "小炒腰花": (35, "荤菜"),
            "火爆腰花": (35, "荤菜"),
            "梅菜扣肉": (45, "荤菜"),
            "烟笋炒腊肉": (32, "荤菜"),
            "铁板姜葱牛肉": (38, "荤菜"),
            "椒盐虾": (45, "荤菜"),
            "麻辣牛展": (46, "荤菜"),
            "土匪猪肝": (28, "荤菜"),
            "双色鱼头": (42, "荤菜"),
            "剁椒鱼头": (42, "荤菜"),
            "韭菜花炒河虾": (35, "荤菜"),
            "外婆菜炒鸡蛋": (25, "荤菜"),
            "支竹牛腩煲": (35, "荤菜"),
            "支竹鱼腩煲": (30, "荤菜"),
            "宫爆鸡丁": (25, "荤菜"),
            "土豆焖排骨": (35, "荤菜"),
            "土豆焖鸡": (28, "荤菜"),
            "攸县香干炒五花肉": (28, "荤菜"),
            "青椒炒猪耳": (32, "荤菜"),
            "蚂蚁上树": (22, "荤菜"),
            "烟笋炒五花肉": (30, "荤菜"),
            "番茄牛肉": (32, "荤菜"),
            "金针菇日本豆腐煲": (28, "荤菜"),
            "鱼香肉丝": (25, "荤菜"),
            "鱼香茄子煲": (22, "素菜"),
            "土豆烧茄子": (22, "素菜"),
            "茄角之恋": (20, "素菜"),
            "红烧茄子": (20, "素菜"),
            "干煸菜花": (20, "素菜"),
            "干煸四季豆": (20, "素菜"),
            "凉瓜煎蛋": (20, "素菜"),
            "凉瓜炒蛋": (20, "素菜"),
            "韭莱炒蛋": (20, "素菜"),
            "酸辣土豆丝": (20, "素菜"),
            "番茄炒蛋": (20, "素菜"),
            "生拍黄瓜": (20, "素菜"),
            "麻婆豆腐": (20, "素菜"),
            "蒜蓉炒时蔬": (20, "素菜")
        }
        
        # 初始化变量
        self.menu_items = self.default_menu.copy()  # 使用默认菜单的副本
        self.selected_items = []
        self.selected_dishes = {}
        
        # 创建页面菜单（移到加载菜单之前）
        self.page_menu = tk.Menu(self.root, tearoff=0)
        
        # 设置配置文件路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe，配置文件保存在用户目录下的 MenuApp 文件夹
            config_dir = os.path.join(os.path.expanduser('~'), 'MenuApp')
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            self.config_file = os.path.join(config_dir, 'menu_config.txt')
        else:
            # 如果是python脚本，配置文件保存在当前目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.config_file = os.path.join(script_dir, 'menu_config.txt')
        
        # 确保配置文件目录存在
        config_dir = os.path.dirname(self.config_file)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        print(f"配置文件路径: {self.config_file}")  # 添加调试信息
        
        # 添加当前页面名称变量
        self.current_page = "佳佳美食"
        
        # 添加页面管理字典，用于存储不同页面的菜单
        self.pages = {
            "佳佳美食": self.menu_items
        }
        
        # 初始化价格权重配置
        self.price_weights = {
            "20-25": 70,  # 修改默认概率为70%
            "26-30": 25,  # 修改默认概率为25%
            "31-35": 4,   # 修改默认概率为4%
            "36+": 1      # 修改默认概率为1%
        }
        
        # 加载价格权重配置
        self.load_price_weights()
        
        # 加载保存的菜单
        self.load_menu()
        
        # 创建右键菜单
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="添加", command=self.add_dish)
        self.context_menu.add_command(label="修改", command=self.edit_selected_dish)
        self.context_menu.add_command(label="删除", command=self.delete_selected_dish)
        
        # 绑定关闭窗口事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 移除自动检查更新
        # self.check_for_updates()  # 删除这行
        
        # 创建界面组件
        self.create_widgets()
        
        # 更新菜单显示
        self.update_menu_display()
        
        # 添加禁用权重的配置
        self.disable_weights = False  # 默认不禁用
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=(10, 10, 10, 0))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        
        # 顶部按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, pady=(0, 10))  # 底部间距10
        button_frame.grid_configure(sticky='n')
        main_frame.grid_rowconfigure(0, weight=0)
        
        # 按钮容器
        buttons_container = ttk.Frame(button_frame)
        buttons_container.pack(expand=True)
        
        # 创建统一样式的按钮
        button_style = {
            'width': 8,  # 统一按钮宽度
            'padding': (5, 2)  # 内部填充
        }
        
        # 按钮布局
        ttk.Button(
            buttons_container, 
            text="导入菜单", 
            command=self.import_menu,
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_container, 
            text="导出菜单", 
            command=self.export_menu,
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        # 页面选择按钮
        self.page_button = ttk.Button(
            buttons_container, 
            text=self.current_page,  # 使用当前页面名称
            **button_style,
            command=lambda: self.page_menu.post(
                self.page_button.winfo_rootx(),
                self.page_button.winfo_rooty() + self.page_button.winfo_height()
            )
        )
        self.page_button.pack(side=tk.LEFT, padx=5)
        
        # 更新页面菜单
        self.update_page_menu()
        
        # 设置按钮改为帮助按钮
        self.settings_button = ttk.Button(
            buttons_container, 
            text="帮助", 
            command=self.show_settings,
            **button_style
        )
        self.settings_button.pack(side=tk.LEFT, padx=5)
        
        # 菜单列表框架
        self.menu_frame = ttk.LabelFrame(main_frame, text=f"{self.current_page}", padding="5")
        self.menu_frame.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        self.menu_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # 创建树形视图
        columns = ('选择', '序号', '名称', '价格', '类型')
        self.tree = ttk.Treeview(self.menu_frame, columns=columns, show='headings')
        
        # 设置列标题和宽度
        self.tree.heading('选择', text='选择')
        self.tree.heading('序号', text='序号')
        self.tree.heading('名称', text='菜品名称')
        self.tree.heading('价格', text='价格')
        self.tree.heading('类型', text='类型')
        
        self.tree.column('选择', width=40, anchor='center')
        self.tree.column('序号', width=40, anchor='center')
        self.tree.column('名称', width=120, anchor='center')
        self.tree.column('价格', width=60, anchor='center')
        self.tree.column('类型', width=60, anchor='center')
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.menu_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 添加点击事件处理
        self.tree.bind('<Button-1>', self.on_tree_click)
        
        # 绑定右键菜单
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # 随机点菜框架
        random_frame = ttk.LabelFrame(main_frame, text="随机点菜", padding="5")
        random_frame.grid(row=2, column=0, pady=(0, 10), sticky=(tk.W, tk.E))  # 底部间距10
        random_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=0)
        
        # 输入框架
        input_frame = ttk.Frame(random_frame)
        input_frame.grid(row=0, column=0, pady=5)
        input_frame.grid_configure(sticky='ew')
        random_frame.grid_columnconfigure(0, weight=1)
        
        # 输入控件容器
        input_container = ttk.Frame(input_frame)
        input_container.pack(expand=True)
        
        ttk.Label(input_container, text="菜品总数:").pack(side=tk.LEFT, padx=5)
        self.dish_count = ttk.Entry(input_container, width=5)
        self.dish_count.pack(side=tk.LEFT, padx=5)
        
        self.include_veg_var = tk.BooleanVar(value=True)
        self.include_veg_check = ttk.Checkbutton(
            input_container, 
            text="素菜",
            variable=self.include_veg_var
        )
        self.include_veg_check.pack(side=tk.LEFT, padx=5)
        
        # 在 input_container 中添加金额限制输入框
        ttk.Label(input_container, text="金额限制:").pack(side=tk.LEFT, padx=5)
        self.price_limit = ttk.Entry(input_container, width=5)
        self.price_limit.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_container, text="随机选择", command=self.random_select).pack(side=tk.LEFT, padx=5)
        
        # 结果框架
        result_frame = ttk.LabelFrame(main_frame, text="已选菜品", padding="5")
        result_frame.grid(row=3, column=0, pady=(0, 0), sticky=(tk.W, tk.E))  # 无间距
        result_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=0)
        
        # 结果文本框
        self.result_text = tk.Text(
            result_frame, 
            width=35,
            height=10,
            state='disabled',
            bg='#F0F0F0',
            relief='flat'
        )
        self.result_text.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E))
        
        # 在总价标签旁添加人数输入和人均价格标签
        price_frame = ttk.Frame(result_frame)
        price_frame.grid(row=1, column=0, pady=5)
        
        # 总价标签
        self.total_price_label = ttk.Label(
            price_frame, 
            text="总价: 0元", 
            font=('Arial', 12, 'bold'),
            foreground='red'
        )
        self.total_price_label.pack(side=tk.LEFT, padx=5)
        
        # 人数输入框
        ttk.Label(price_frame, text="人数:").pack(side=tk.LEFT, padx=5)
        self.people_count = ttk.Entry(price_frame, width=3)
        self.people_count.insert(0, "1")
        self.people_count.pack(side=tk.LEFT)
        
        # 人均价格标签
        self.avg_price_label = ttk.Label(
            price_frame, 
            text="人均: 0元",
            font=('Arial', 12, 'bold'),
            foreground='blue'
        )
        self.avg_price_label.pack(side=tk.LEFT, padx=5)
        
        # 绑定人数输入框的变化事件
        self.people_count.bind('<KeyRelease>', self.update_avg_price)

        # 版本号标签
        version_label = ttk.Label(
            self.root,
            text=f"v{self.VERSION}",
            font=('Arial', 8),
            foreground='gray'
        )
        version_label.grid(row=1, column=0, sticky=(tk.E), padx=15, pady=0)

    def add_dish(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("添加菜品")
        add_window.resizable(False, False)
        
        # 设置添加窗口的大小
        add_window.geometry("250x200")
        
        # 设置图标
        icon_path = self.get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            add_window.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window(add_window)
        
        # 创建主框架并居中
        main_frame = ttk.Frame(add_window, padding="10")
        main_frame.pack(expand=True)
        
        # 创建输入框和标签
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(expand=True)
        
        # 菜品名称
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill='x', pady=5)
        ttk.Label(name_frame, text="菜名:").pack(side=tk.LEFT, padx=5)
        name_entry = ttk.Entry(name_frame, width=15)
        name_entry.pack(side=tk.LEFT, padx=5)
        
        # 价格
        price_frame = ttk.Frame(input_frame)
        price_frame.pack(fill='x', pady=5)
        ttk.Label(price_frame, text="价格:").pack(side=tk.LEFT, padx=5)
        price_entry = ttk.Entry(price_frame, width=15)
        price_entry.pack(side=tk.LEFT, padx=5)
        
        # 类型
        type_frame = ttk.Frame(input_frame)
        type_frame.pack(fill='x', pady=5)
        ttk.Label(type_frame, text="类型:").pack(side=tk.LEFT, padx=5)
        type_combo = ttk.Combobox(type_frame, values=["荤菜", "素菜"], width=10)
        type_combo.pack(side=tk.LEFT, padx=5)
        type_combo.set("荤菜")
        
        def save_dish():
            name = name_entry.get().strip()
            try:
                price = float(price_entry.get().strip())
                if name and price > 0:
                    # 确保价格是整数
                    price = int(price)
                    dish_type = type_combo.get()
                    
                    # 检查菜品是否已存在
                    if name in self.menu_items:
                        if not messagebox.askyesno("警告", f"菜品 {name} 已存在，是否覆盖？"):
                            return
                    
                    # 添加新菜品
                    self.menu_items[name] = (price, dish_type)
                    
                    # 更新显示并保存
                    self.update_menu_display()
                    
                    # 定位到新添加的菜品
                    for item in self.tree.get_children():
                        if self.tree.item(item)['values'][2] == name:
                            self.tree.selection_set(item)
                            self.tree.focus(item)
                            self.tree.see(item)
                            break
                    
                    add_window.destroy()
                    messagebox.showinfo("成功", f"已添加菜品：{name}")
                else:
                    messagebox.showwarning("警告", "请输入有效的菜品信息！")
            except ValueError:
                messagebox.showwarning("警告", "请输入有效的价格！")
                
        # 保存按钮居中
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=20)
        ttk.Button(button_frame, text="保存", command=save_dish).pack(expand=True)

    def on_tree_click(self, event):
        """点击树形视图时的处理"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":  # 点击任意单元格
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            if item:
                values = self.tree.item(item)['values']
                name = values[2]  # 菜品名称在第三列
                
                if column == '#1':  # 点击选择列
                    # 保存当前选中项
                    selected_items = self.tree.selection()
                    
                    # 切换勾选状态
                    if name in self.selected_dishes:
                        del self.selected_dishes[name]
                    else:
                        self.selected_dishes[name] = True
                    
                    # 更新显示(会处理菜品位置)
                    self.update_menu_display()
                    self.update_selected_display()
                    
                    # 恢复之前的选中状态
                    if selected_items:
                        self.tree.selection_set(selected_items)
                    
                    # 添加自动保存
                    self.save_menu()
                else:  # 点击其他列
                    # 只改变选中状态
                    self.tree.selection_set(item)
                    self.tree.focus(item)

    def update_selected_display(self):
        # 更新已选菜品显示
        display_text = ""
        total_price = 0
        
        # 获取所有已选菜品
        selected_items = []
        for name in self.selected_dishes:
            if name in self.menu_items:
                price = self.menu_items[name][0]
                selected_items.append((name, price))
                total_price += price

        # 显示已选菜品
        for name, price in selected_items:
            spaces = " " * (12 - len(name))
            display_text += f"{name}{spaces}{int(price)}元\n"

        # 更新显示
        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, display_text)
        self.result_text.configure(state='disabled')
        
        # 更新总价
        self.total_price_label.configure(text=f"总价: {int(total_price)}元")
        
        # 在函数末尾添加自动保存
        self.save_menu()

    def update_menu_display(self):
        # 清空现有显示
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 将菜品按类型分组
        meat_dishes = []  # 荤菜
        veg_dishes = []   # 素菜
        
        # 分类菜品
        for name, (price, dish_type) in self.menu_items.items():
            if dish_type == "荤菜":
                meat_dishes.append((name, price))
            else:
                veg_dishes.append((name, price))
        
        # 按名称排序
        meat_dishes.sort(key=lambda x: x[0])
        veg_dishes.sort(key=lambda x: x[0])
        
        # 将所有已选菜品放在最前面，未选菜品按类型分组
        selected_dishes = []  # 所有已选菜品
        unselected_meat = []  # 未选荤菜
        unselected_veg = []   # 未选素菜
        
        # 分类所有菜品
        for name, price in meat_dishes + veg_dishes:
            if name in self.selected_dishes:
                selected_dishes.append((name, price, self.menu_items[name][1]))  # 包含类型信息
            elif self.menu_items[name][1] == "荤菜":
                unselected_meat.append((name, price))
            else:
                unselected_veg.append((name, price))
        
        serial_number = 1  # 序号计数器
        
        # 显示已选菜品(在最顶部)
        for name, price, dish_type in selected_dishes:
            self.tree.insert('', 'end', tags=(name,), 
                            values=('✅', str(serial_number), name, f"{int(price)}", dish_type))
            serial_number += 1
        
        # 显示未选荤菜
        for name, price in unselected_meat:
            self.tree.insert('', 'end', tags=(name,), 
                            values=('⬜', str(serial_number), name, f"{int(price)}", "荤菜"))
            serial_number += 1
        
        # 显示未选素菜
        for name, price in unselected_veg:
            self.tree.insert('', 'end', tags=(name,), 
                            values=('⬜', str(serial_number), name, f"{int(price)}", "素菜"))
            serial_number += 1

        # 在函数末尾添加自动保存
        self.save_menu()

    def import_menu(self):
        file_path = filedialog.askopenfilename(
            title="选择菜单文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    new_menu = {}
                    for line in file:
                        name, price, dish_type = line.strip().split(',')
                        new_menu[name] = (float(price), dish_type)
                    if new_menu:
                        print(f"导入菜单到页面: {self.current_page}")
                        # 更新当前页面的菜单
                        self.pages[self.current_page] = new_menu
                        self.menu_items = new_menu
                        self.selected_dishes.clear()
                        
                        # 先保存配置
                        if self.save_menu():
                            print(f"导入菜单保存成功")
                            # 再更新显示
                            self.update_menu_display()
                            self.update_selected_display()
                            messagebox.showinfo("成功", "菜单导入成功！")
                        else:
                            print(f"导入菜单保存失败")
                            messagebox.showerror("错误", "菜单导入失败：保存配置时出错")
            except Exception as e:
                error_window = messagebox.showerror("错误", f"导入失败：{str(e)}")
                if error_window:
                    self.center_window(error_window)

    def export_menu(self):
        file_path = filedialog.asksaveasfilename(
            title="保存菜单",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    for name, (price, dish_type) in self.menu_items.items():
                        file.write(f"{name},{price},{dish_type}\n")
                messagebox.showinfo("成功", "菜单导出成功！")
            except Exception as e:
                # 创建错误消息窗口并居中显示
                error_window = messagebox.showerror("错误", f"导出失败：{str(e)}")
                if error_window:
                    self.center_window(error_window)
                
    def random_select(self):
        """随机选择菜品"""
        if not self.menu_items:
            messagebox.showwarning("警告", "请先导入或添加菜品！")
            return
            
        try:
            # 获取用户输入的菜品数量和金额限制
            count = int(self.dish_count.get().strip())
            price_limit = self.price_limit.get().strip()
            
            if count <= 0:
                messagebox.showwarning("警告", "请输入大于0的数字！")
                return
            
            # 清空之前的选择
            self.selected_items = []
            
            # 获取已选菜品（勾选的）
            pre_selected = []
            pre_selected_total = 0
            for name in self.selected_dishes:
                if name in self.menu_items:
                    price = self.menu_items[name][0]
                    pre_selected.append((name, price))
                    pre_selected_total += price
            
            # 如果设置了金额限制，检查已选菜品是否超过限制
            if price_limit:
                price_limit = float(price_limit)
                if pre_selected_total > price_limit:
                    messagebox.showwarning("警告", f"已选菜品总价({pre_selected_total}元)超过金额限制({price_limit}元)！")
                    return
            
            # 计算还需要选择的菜品数量
            remaining_count = count - len(pre_selected)
            
            # 如果已选数量超过要求数量，直接返回
            if remaining_count < 0:
                messagebox.showwarning("警告", "已选菜品数量超过要求！")
                return
            elif remaining_count == 0:
                self.selected_items = pre_selected
                self.update_selected_display()
                return
            
            # 最大尝试次数，防止无限循环
            max_attempts = 50
            attempts = 0
            
            while attempts < max_attempts:
                attempts += 1
                
                # 获取可选菜品（排除已选菜品）
                available_meat = [(name, price) 
                                for name, (price, dish_type) in self.menu_items.items()
                                if dish_type == "荤菜" and name not in self.selected_dishes]
                
                available_veg = [(name, price) 
                               for name, (price, dish_type) in self.menu_items.items()
                               if dish_type == "素菜" and name not in self.selected_dishes]
                
                # 根据是否包含素菜进行选择
                if self.include_veg_var.get() and available_veg:
                    veg_count = min(max(1, remaining_count // 3), len(available_veg))
                    meat_count = min(remaining_count - veg_count, len(available_meat))
                    
                    if meat_count + veg_count < remaining_count:
                        messagebox.showwarning("警告", "可选菜品数量不足！")
                        return
                    
                    # 根据价格权重进行随机选择
                    meat_dishes = []
                    meat_weights = []
                    for name, price in available_meat:
                        meat_dishes.append(name)
                        meat_weights.append(self.get_price_weight(price))
                    
                    veg_dishes = []
                    veg_weights = []
                    for name, price in available_veg:
                        veg_dishes.append(name)
                        veg_weights.append(self.get_price_weight(price))
                    
                    # 随机选择荤菜和素菜
                    selected_meat = []
                    selected_veg = []
                    
                    # 确保选择指定数量的荤菜
                    while len(selected_meat) < meat_count:
                        name = random.choices(meat_dishes, weights=meat_weights, k=1)[0]
                        for dish_name, price in available_meat:
                            if dish_name == name and (dish_name, price) not in selected_meat:
                                selected_meat.append((dish_name, price))
                                break
                    
                    # 确保选择指定数量的素菜
                    while len(selected_veg) < veg_count:
                        name = random.choices(veg_dishes, weights=veg_weights, k=1)[0]
                        for dish_name, price in available_veg:
                            if dish_name == name and (dish_name, price) not in selected_veg:
                                selected_veg.append((dish_name, price))
                                break
                    
                    current_selection = pre_selected + selected_meat + selected_veg
                else:
                    # 如果不包含素菜，全部选择荤菜
                    if len(available_meat) < remaining_count:
                        messagebox.showwarning("警告", "可选荤菜数量不足！")
                        return
                    
                    # 根据价格权重进行随机选择
                    meat_dishes = []
                    meat_weights = []
                    for name, price in available_meat:
                        meat_dishes.append(name)
                        meat_weights.append(self.get_price_weight(price))
                    
                    # 随机选择荤菜
                    selected_meat = []
                    while len(selected_meat) < remaining_count:
                        name = random.choices(meat_dishes, weights=meat_weights, k=1)[0]
                        for dish_name, price in available_meat:
                            if dish_name == name and (dish_name, price) not in selected_meat:
                                selected_meat.append((dish_name, price))
                                break
                    
                    current_selection = pre_selected + selected_meat
                
                # 计算当前选择的总价
                total_price = sum(price for _, price in current_selection)
                
                # 如果没有设置金额限制或总价在限制范围内，接受当前选择
                if not price_limit or total_price <= price_limit:
                    self.selected_items = current_selection
                    break
            
            # 如果达到最大尝试次数仍未找到合适组合
            if attempts >= max_attempts:
                messagebox.showwarning("警告", f"无法在金额限制({price_limit}元)内找到合适的菜品组合！")
                return
            
            # 更新显示
            display_text = ""
            notification_text = ""
            
            # 计算总价并显示所有菜品
            total_price = sum(price for _, price in self.selected_items)
            
            # 显示所有菜品（添加序号）
            for i, (name, price) in enumerate(self.selected_items, 1):
                spaces = " " * (12 - len(name))
                display_text += f"{i}. {name}{spaces}{int(price)}元\n"
                notification_text += f"{name}, "
            
            # 移除最后的逗号和空格
            notification_text = notification_text.rstrip(", ")
            
            # 更新结果显示
            self.result_text.configure(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, display_text)
            self.result_text.configure(state='disabled')
            
            # 更新总价标签
            self.total_price_label.configure(text=f"总价: {int(total_price)}元")
            
            # 更新人均价格
            self.update_avg_price()
            
            # 准备剪贴板文本
            clip_text = ""
            for i, (name, _) in enumerate(self.selected_items, 1):
                clip_text += f"{i}. {name}\n"
            
            # 添加空行和回复提示
            clip_text += "\n收到请回复"
            
            # 复制到剪贴板
            self.root.clipboard_clear()
            self.root.clipboard_append(clip_text)
            
            # 显示通知
            total_selected = len(self.selected_items)
            if total_selected > 0:
                self.save_menu()
                if HAS_WINOTIFY:
                    # 获取图标路径
                    icon_path = self.get_resource_path("icon.ico")
                    # 显示 Windows 通知
                    toast = Notification(
                        app_id="今天吃什么",
                        title="点菜完成",
                        msg=f"已选择{total_selected}个菜品：\n{notification_text}\n\n总价: {int(total_price)}元\n已复制到剪贴板",
                        duration="short",
                        icon=icon_path if os.path.exists(icon_path) else None
                    )
                    toast.show()
                else:
                    # 使用消息框
                    messagebox.showinfo(
                        "点菜完成",
                        f"已选择{total_selected}个菜品：\n{notification_text}\n\n总价: {int(total_price)}元\n已复制到剪贴板"
                    )
            
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的数字！")

    def load_menu(self):
        """从配置文件加载菜单"""
        try:
            if os.path.exists(self.config_file):
                print(f"正在从 {self.config_file} 加载配置")
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    current_page = None
                    self.pages = {}  # 清空现有页面
                    self.selected_dishes.clear()
                    
                    # 读取文件内容
                    content = file.read()
                    print(f"配置文件内容:\n{content}")
                    
                    # 重置文件指针
                    file.seek(0)
                    
                    # 读取所有页面和菜品
                    for line in file:
                        line = line.strip()
                        if not line:
                            continue
                        
                        if line.startswith("[Page:"):
                            current_page = line[6:-1]  # 提取页面名称
                            print(f"发现页面: {current_page}")
                            if current_page not in self.pages:
                                print(f"创建页面: {current_page}")
                                self.pages[current_page] = {}
                            continue
                        elif line == "[Selected]":
                            current_page = None
                            continue
                        
                        if current_page is not None:  # 处理菜品数据
                            try:
                                name, price, dish_type = line.split(',')
                                self.pages[current_page][name] = (float(price), dish_type)
                                print(f"加载菜品: {name} 到页面 {current_page}")
                            except Exception as e:
                                print(f"解析菜品失败: {line}, 错误: {str(e)}")
                        else:  # [Selected] 部分
                            self.selected_dishes[line] = True
                    
                    print(f"加载完成，所有页面: {list(self.pages.keys())}")
                    
                    # 如果没有加载到任何页面，使用默认菜单
                    if not self.pages:
                        print("没有加载到任何页面，使用默认菜单")
                        self.pages["佳佳美食"] = self.default_menu.copy()
                    
                    # 尝试加载上次的页面状态
                    last_state_file = os.path.join(os.path.dirname(self.config_file), 'last_state.json')
                    if os.path.exists(last_state_file):
                        try:
                            with open(last_state_file, 'r', encoding='utf-8') as f:
                                last_state = json.load(f)
                                if last_state['current_page'] in self.pages:
                                    self.current_page = last_state['current_page']
                                    print(f"恢复到上次的页面: {self.current_page}")
                                else:
                                    self.current_page = next(iter(self.pages.keys()))
                        except Exception as e:
                            print(f"加载上次状态失败: {str(e)}")
                            self.current_page = next(iter(self.pages.keys()))
                    else:
                        self.current_page = next(iter(self.pages.keys()))
                    
                    # 更新当前菜单和标题
                    self.menu_items = self.pages[self.current_page]
                    if hasattr(self, 'menu_frame'):
                        self.menu_frame.configure(text=f"{self.current_page}")  # 只显示页面名称
                    
                    # 更新页面菜单
                    self.update_page_menu()
                    
                    print(f"加载配置成功")
                    print(f"已加载页面: {list(self.pages.keys())}")
                    print(f"当前页面: {self.current_page}")
                    print(f"当前菜单: {self.menu_items}")
                    
            else:
                print(f"配置文件不存在: {self.config_file}")
                # 如果配置文件不存在，使用默认菜单
                self.pages = {"佳佳美食": self.default_menu.copy()}
                self.menu_items = self.default_menu.copy()
                self.current_page = "佳佳美食"
                self.update_page_menu()
                # 保存初始配置
                self.save_menu()
                
        except Exception as e:
            print(f"加载菜单失败: {str(e)}")
            # 出错时使用默认菜单
            self.pages = {"佳佳美食": self.default_menu.copy()}
            self.menu_items = self.default_menu.copy()
            self.current_page = "佳佳美食"
            self.update_page_menu()

    def save_menu(self):
        """保存菜单到配置文件"""
        try:
            # 确保配置文件所在目录存在
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            print(f"正在保存配置到: {self.config_file}")
            print(f"当前页面: {self.current_page}")
            print(f"所有页面: {list(self.pages.keys())}")
            print(f"当前页面菜单内容: {self.menu_items}")
            
            # 确保当前页面的菜单内容已同步到pages中
            self.pages[self.current_page] = self.menu_items.copy()
            
            # 保存菜单
            with open(self.config_file, 'w', encoding='utf-8') as file:
                # 保存所有页面
                for page_name, menu_items in self.pages.items():
                    print(f"保存页面: {page_name}, 菜品数量: {len(menu_items)}")  # 调试信息
                    file.write(f"[Page:{page_name}]\n")
                    # 确保菜品信息被正确写入
                    for name, (price, dish_type) in menu_items.items():
                        file.write(f"{name},{price},{dish_type}\n")
                    file.write("\n")  # 页面之间添加空行
                
                # 保存选中状态部分
                file.write("[Selected]\n")
                for name in self.selected_dishes:
                    file.write(f"{name}\n")
            
            print(f"配置保存成功: {self.config_file}")
            print(f"已保存页面: {list(self.pages.keys())}")
            return True
        except Exception as e:
            error_msg = f"保存失败:\n路径: {self.config_file}\n错误: {str(e)}"
            print(error_msg)
            messagebox.showerror("错误", error_msg)
            return False

    def on_closing(self):
        """程序关闭时的处理"""
        try:
            print("正在保存配置...")
            # 保存当前页面信息到配置文件
            with open(os.path.join(os.path.dirname(self.config_file), 'last_state.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'current_page': self.current_page,
                    'selected_dishes': list(self.selected_dishes.keys())
                }, f, ensure_ascii=False, indent=2)
            print(f"保存当前页面状态: {self.current_page}")
            
            # 保存菜单配置
            if self.save_menu():
                print("菜单配置保存成功")
            else:
                print("菜单配置保存失败")
            
            # 保存价格权重配置
            try:
                self.save_price_weights()
                print("价格权重配置保存成功")
            except Exception as e:
                print(f"价格权重配置保存失败: {str(e)}")
            
            print("所有配置保存完成")
        except Exception as e:
            print(f"保存配置时发生错误: {str(e)}")
            messagebox.showerror("错误", f"保存配置时发生错误：{str(e)}")
        finally:
            self.root.destroy()

    def show_context_menu(self, event):
        """显示右键菜单"""
        # 获取点击位置的项
        item = self.tree.identify_row(event.y)
        if item:
            # 先取消所有选择
            self.tree.selection_clear()
            # 选中右键点击的项
            self.tree.selection_set(item)
            self.tree.focus(item)
            # 显示菜单
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()

    def delete_selected_dish(self):
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                return
                
            item = selected_items[0]
            values = self.tree.item(item)['values']
            if not values or len(values) < 3:
                return
                
            name = str(values[2])  # 菜品名称在第三列
            
            # 确认删除
            if messagebox.askyesno("确认删除", f"确定要删除 {name} 吗？"):
                # 从菜单中删除
                if name in self.menu_items:
                    del self.menu_items[name]
                    # 从已选菜品中删除
                    if name in self.selected_dishes:
                        del self.selected_dishes[name]
                    
                    # 更新显示
                    self.update_menu_display()
                    self.update_selected_display()
                    
                    # 保存更改
                    self.save_menu()
                    
                    messagebox.showinfo("成功", f"已删除菜品：{name}")
                else:
                    messagebox.showwarning("警告", f"未找到菜品：{name}")
        except Exception as e:
            print(f"Error during deletion: {str(e)}")
            messagebox.showerror("错误", f"删除失败：{str(e)}")

    def edit_selected_dish(self):
        """修改选中的菜品"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        item = selected_items[0]
        values = self.tree.item(item)['values']
        if not values or len(values) < 5:
            return
            
        old_name = values[2]  # 菜品名称在第三列
        old_price = values[3]  # 价格在第四列
        old_type = values[4]  # 类型在第五列
        
        # 创建修改窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title("修改菜品")
        edit_window.resizable(False, False)
        
        # 设置修改窗口的大小
        edit_window.geometry("250x200")
        
        # 设置图标
        icon_path = self.get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            edit_window.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window(edit_window)
        
        # 创建主框架并居中
        main_frame = ttk.Frame(edit_window, padding="10")
        main_frame.pack(expand=True)
        
        # 创建输入框和标签
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(expand=True)
        
        # 菜品名称
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill='x', pady=5)
        ttk.Label(name_frame, text="菜名:").pack(side=tk.LEFT, padx=5)
        name_entry = ttk.Entry(name_frame, width=15)
        name_entry.pack(side=tk.LEFT, padx=5)
        name_entry.insert(0, old_name)  # 设置当前值
        
        # 价格
        price_frame = ttk.Frame(input_frame)
        price_frame.pack(fill='x', pady=5)
        ttk.Label(price_frame, text="价格:").pack(side=tk.LEFT, padx=5)
        price_entry = ttk.Entry(price_frame, width=15)
        price_entry.pack(side=tk.LEFT, padx=5)
        price_entry.insert(0, old_price)  # 设置当前值
        
        # 类型
        type_frame = ttk.Frame(input_frame)
        type_frame.pack(fill='x', pady=5)
        ttk.Label(type_frame, text="类型:").pack(side=tk.LEFT, padx=5)
        type_combo = ttk.Combobox(type_frame, values=["荤菜", "素菜"], width=10)
        type_combo.pack(side=tk.LEFT, padx=5)
        type_combo.set(old_type)  # 设置当前值
        
        def save_edit():
            new_name = name_entry.get().strip()
            try:
                new_price = float(price_entry.get().strip())
                if new_name and new_price > 0:
                    # 确保价格是整数
                    new_price = int(new_price)
                    new_type = type_combo.get()
                    
                    # 检查是否真的有修改
                    if (new_name == old_name and 
                        new_price == int(old_price) and 
                        new_type == old_type):
                        edit_window.destroy()
                        return
                    
                    # 保存选中状态
                    was_selected = old_name in self.selected_dishes
                    
                    try:
                        print(f"开始修改菜品: {old_name}")
                        print(f"当前菜单状态: {self.menu_items}")
                        
                        # 直接修改当前菜品
                        self.menu_items[old_name] = (new_price, new_type)
                        
                        # 如果修改了名称，需要更新键名
                        if new_name != old_name:
                            # 使用字典推导式创建新的菜单，保持其他菜品不变
                            self.menu_items = {
                                new_name if k == old_name else k: v 
                                for k, v in self.menu_items.items()
                            }
                            
                            # 更新选中状态
                            if was_selected:
                                del self.selected_dishes[old_name]
                                self.selected_dishes[new_name] = True
                        
                        print(f"更新后的菜单状态: {self.menu_items}")
                        
                        # 更新显示
                        self.update_menu_display()
                        self.update_selected_display()
                        
                        # 保存更改
                        self.save_menu()
                        
                        edit_window.destroy()
                        messagebox.showinfo("成功", f"已修改菜品：{new_name}")
                    except Exception as e:
                        print(f"保存失败，错误信息: {str(e)}")
                        messagebox.showerror("错误", f"保存失败：{str(e)}")
                        return
                else:
                    messagebox.showwarning("警告", "请输入有效的菜品信息！")
            except ValueError:
                messagebox.showwarning("警告", "请输入有效的价格！")

        # 保存按钮居中
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=20)
        ttk.Button(button_frame, text="保存", command=save_edit).pack(expand=True)

    def show_price_weights(self):
        """显示价格区间概率设置窗口"""
        weights_window = tk.Toplevel(self.root)
        weights_window.title("价格区间概率设置")
        weights_window.resizable(False, False)
        weights_window.geometry("280x300")
        
        # 设置图标
        icon_path = self.get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            weights_window.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window(weights_window)
        
        # 创建主框架
        main_frame = ttk.Frame(weights_window)
        main_frame.pack(fill='both', expand=True)
        
        # 创建内容框架
        content_frame = ttk.Frame(main_frame, padding="20")
        content_frame.pack(fill='both')
        
        # 说明标签
        ttk.Label(content_frame, 
                 text="设置不同价格区间的随机概率\n(各区间概率之和需等于100%)", 
                 justify='center').pack(pady=(0, 20))
        
        # 创建输入框容器
        entries_frame = ttk.Frame(content_frame)
        entries_frame.pack()
        
        # 错误提示标签
        error_label = ttk.Label(content_frame, text="", foreground="red")
        error_label.pack(pady=5)
        
        # 添加禁用选项
        disable_var = tk.BooleanVar(value=self.disable_weights)
        disable_check = ttk.Checkbutton(
            content_frame,
            text="禁用权重概率（所有价格区间概率相等）",
            variable=disable_var,
            command=lambda: update_entries_state()
        )
        disable_check.pack(pady=5)

        def update_entries_state():
            """更新输入框的启用/禁用状态"""
            state = 'disabled' if disable_var.get() else 'normal'
            for entry in entries.values():
                entry.configure(state=state)
            
            # 如果是禁用状态，显示将要设置的值（25%）
            if disable_var.get():
                for entry in entries.values():
                    entry.configure(state='normal')  # 临时启用以更新值
                    entry.delete(0, tk.END)
                    entry.insert(0, "25")
                    entry.configure(state='disabled')  # 重新禁用
            else:
                # 恢复到当前保存的值
                for price_range, entry in entries.items():
                    entry.configure(state='normal')
                    entry.delete(0, tk.END)
                    entry.insert(0, str(self.price_weights[price_range]))
        
        def validate_and_save():
            try:
                # 保存禁用状态
                self.disable_weights = disable_var.get()
                
                if not self.disable_weights:
                    # 如果不禁用，验证并保存输入的值
                    new_weights = {}
                    total = 0
                    for price_range, entry in entries.items():
                        value = entry.get().strip()
                        # 检查是否为空
                        if not value:
                            error_label.config(text=f"{price_range}元区间不能为空")
                            return
                        
                        # 检查是否为整数
                        try:
                            value = int(float(value))
                        except ValueError:
                            error_label.config(text=f"{price_range}元区间请输入整数")
                            return
                        
                        # 检查是否为负数
                        if value < 0:
                            error_label.config(text=f"{price_range}元区间不能为负数")
                            return
                        
                        # 检查是否超过100
                        if value > 100:
                            error_label.config(text=f"{price_range}元区间不能超过100%")
                            return
                        
                        new_weights[price_range] = value
                        total += value
                    
                    # 检查总和是否为100
                    if total != 100:
                        error_label.config(text=f"所有概率之和必须等于100%（当前{total}%）")
                        return
                    
                    # 保存新的权重值
                    self.price_weights = new_weights
                
                # 保存配置
                self.save_price_weights()
                weights_window.destroy()
                messagebox.showinfo("成功", "价格区间概率设置已保存")
                
            except Exception as e:
                error_label.config(text=f"输入错误：{str(e)}")
        
        # 创建价格区间的输入框
        entries = {}
        for i, price_range in enumerate(self.price_weights.keys()):
            frame = ttk.Frame(entries_frame)
            frame.pack(pady=5)
            
            # 标签
            ttk.Label(frame, text=f"{price_range}元: ", width=10).pack(side=tk.LEFT)
            
            # 输入框
            entry = ttk.Entry(frame, width=10, justify='center')
            entry.insert(0, str(self.price_weights[price_range]))
            entry.pack(side=tk.LEFT, padx=5)
            
            # 百分比符号
            ttk.Label(frame, text="%").pack(side=tk.LEFT)
            
            entries[price_range] = entry
            
            # 在36+元那一行下面添加按钮框架
            if price_range == "36+":
                button_frame = ttk.Frame(entries_frame)
                button_frame.pack(pady=10)
                
                # 添加禁用选项（放在保存按钮左边）
                disable_var = tk.BooleanVar(value=self.disable_weights)
                disable_check = ttk.Checkbutton(
                    button_frame,
                    text="禁用权重概率",
                    variable=disable_var,
                    command=lambda: update_entries_state()
                )
                disable_check.pack(side=tk.LEFT, padx=(0, 10))
                
                # 保存按钮
                ttk.Button(button_frame, text="保存", command=validate_and_save, width=8).pack(side=tk.LEFT)
        
        # 根据当前禁用状态更新输入框状态
        update_entries_state()

    def load_price_weights(self):
        """加载价格权重配置"""
        try:
            weights_file = os.path.join(os.path.dirname(self.config_file), 'price_weights.json')
            if os.path.exists(weights_file):
                with open(weights_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        if 'weights' in data:
                            self.price_weights = data['weights']
                        if 'disabled' in data:
                            self.disable_weights = data['disabled']
                    else:
                        # 兼容旧版本的配置文件
                        self.price_weights = data
        except Exception as e:
            print(f"加载价格权重失败: {str(e)}")

    def save_price_weights(self):
        """保存价格权重配置"""
        try:
            weights_file = os.path.join(os.path.dirname(self.config_file), 'price_weights.json')
            with open(weights_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'weights': self.price_weights,
                    'disabled': self.disable_weights
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存价格权重失败: {str(e)}")

    def get_price_weight(self, price):
        """获取指定价格的权重"""
        if self.disable_weights:
            return 25  # 禁用权重时，所有区间概率相等（100/4=25）
        
        # 不禁用时使用设置的权重
        if price <= 25:
            return self.price_weights["20-25"]
        elif price <= 30:
            return self.price_weights["26-30"]
        elif price <= 35:
            return self.price_weights["31-35"]
        else:
            return self.price_weights["36+"]

    def update_avg_price(self, event=None):
        """更新人均价格"""
        try:
            # 获取总价
            total_price = sum(price for _, price in self.selected_items)
            
            # 获取人数
            people = int(self.people_count.get().strip() or "1")
            if people <= 0:
                people = 1
            
            # 计算人均价格
            avg_price = total_price / people
            
            # 如果是整数则显示整数，否则显示一位小数
            if avg_price.is_integer():
                self.avg_price_label.configure(text=f"人均: {int(avg_price)}元")
            else:
                self.avg_price_label.configure(text=f"人均: {avg_price:.1f}元")
            
            # 添加自动保存
            self.save_menu()
        except ValueError:
            self.avg_price_label.configure(text="人均: 0元")

    def check_for_updates(self):
        """检查是否有新版本"""
        try:
            # 从Gitee获取最新版本信息
            response = requests.get(
                "https://gitee.com/api/v5/repos/inueue/menu-app/releases/latest",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                latest_version = data["tag_name"].lstrip("v")
                
                # 比较版本号
                if version.parse(latest_version) > version.parse(self.VERSION):
                    # 查找zip格式的更新包
                    download_url = None
                    for asset in data["assets"]:
                        if asset["name"].endswith(".zip"):
                            download_url = asset["browser_download_url"]
                            break
                    
                    if download_url:
                        if messagebox.askyesno(
                            "发现新版本",
                            f"当前版本：{self.VERSION}\n"
                            f"最新版本：{latest_version}\n\n"
                            "是否下载新版本？"
                        ):
                            self.reliable_vbs_update(download_url, latest_version)
                    else:
                        # 如果没有找到zip包，则提供手动更新链接
                        download_url = data["html_url"]
                        if messagebox.askyesno(
                            "发现新版本",
                            f"当前版本：{self.VERSION}\n"
                            f"最新版本：{latest_version}\n\n"
                            "未找到更新包，是否前往下载页面手动更新？"
                        ):
                            webbrowser.open(download_url)
        except Exception as e:
            print(f"检查更新失败: {str(e)}")

    def reliable_vbs_update(self, download_url, version):
        """使用最可靠的VBS方法实现静默更新"""
        try:
            # 创建进度窗口
            progress_window = tk.Toplevel(self.root)
            progress_window.title("下载更新")
            progress_window.geometry("300x120")
            progress_window.resizable(False, False)
            
            # 设置图标
            icon_path = self.get_resource_path("icon.ico")
            if os.path.exists(icon_path):
                progress_window.iconbitmap(icon_path)
            
            # 居中显示
            self.center_window(progress_window)
            
            # 创建标签和进度条
            status_label = ttk.Label(progress_window, text=f"正在下载 v{version} 更新...", padding=10)
            status_label.pack()
            progress = ttk.Progressbar(progress_window, length=250, mode="indeterminate")
            progress.pack(padx=20, pady=10)
            progress.start()
            
            # 获取程序信息
            app_path = os.path.abspath(sys.argv[0])
            app_dir = os.path.dirname(app_path)
            app_name = os.path.basename(app_path)
            pid = os.getpid()
            
            def download_thread():
                try:
                    # 下载到临时文件夹
                    temp_dir = tempfile.mkdtemp()
                    zip_path = os.path.join(temp_dir, "update.zip")
                    
                    # 下载更新包
                    status_label.config(text=f"正在下载更新文件...")
                    urlretrieve(download_url, zip_path)
                    
                    # 解压文件
                    extract_dir = os.path.join(temp_dir, "extracted")
                    os.makedirs(extract_dir, exist_ok=True)
                    status_label.config(text=f"正在准备更新文件...")
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    
                    # 创建批处理更新文件
                    bat_path = os.path.join(temp_dir, "update.bat")
                    with open(bat_path, "w", encoding="gbk") as f:
                        f.write("@echo off\n")
                        f.write("title 程序更新\n")
                        f.write("color 0A\n")
                        f.write("echo 正在关闭应用程序...\n")
                        f.write(f"taskkill /F /PID {pid} /T >nul 2>&1\n")
                        f.write("echo 正在等待进程结束...\n")
                        f.write("timeout /t 3 /nobreak >nul\n")
                        
                        # 先删除原有EXE文件
                        f.write("echo 正在删除旧版本...\n")
                        f.write(f"del /F /Q \"{app_path}\" >nul 2>&1\n")
                        
                        # 删除可能存在的临时文件
                        f.write(f"del /F /Q \"{app_dir}\\*.pyd\" >nul 2>&1\n")
                        f.write(f"del /F /Q \"{app_dir}\\*.dll\" >nul 2>&1\n")
                        
                        # 查找并复制新的EXE文件
                        found_exe = False
                        for root, dirs, files in os.walk(extract_dir):
                            for file in files:
                                if file.lower().endswith('.exe'):
                                    src_path = os.path.join(root, file)
                                    # 使用原来的文件名而不是下载的文件名
                                    f.write("echo 正在复制新版本...\n")
                                    f.write(f"copy /Y \"{src_path}\" \"{app_path}\" >nul\n")
                                    found_exe = True
                                    break
                            if found_exe:
                                break
                        
                        # 如果没找到EXE，则复制所有文件
                        if not found_exe:
                            f.write("echo 正在复制更新文件...\n")
                            f.write(f"xcopy /E /Y \"{extract_dir}\\*\" \"{app_dir}\\\" >nul\n")
                        
                        # 复制其他可能的资源文件
                        f.write(f"xcopy /E /Y \"{extract_dir}\\*.dll\" \"{app_dir}\\\" >nul 2>&1\n")
                        f.write(f"xcopy /E /Y \"{extract_dir}\\*.pyd\" \"{app_dir}\\\" >nul 2>&1\n")
                        f.write(f"xcopy /E /Y \"{extract_dir}\\*.ico\" \"{app_dir}\\\" >nul 2>&1\n")
                        
                        # 启动应用程序
                        f.write("echo 更新完成! 正在启动新版本...\n")
                        f.write("ping 127.0.0.1 -n 2 >nul\n")  # 短暂延迟
                        f.write(f"cd /d \"{app_dir}\"\n")
                        f.write(f"start \"\" \"{app_path}\"\n")
                        
                        # 清理临时文件
                        f.write("echo 正在清理临时文件...\n")
                        f.write(f"rmdir /S /Q \"{temp_dir}\" >nul 2>&1\n")
                        f.write("echo 更新已完成!\n")
                        f.write("timeout /t 3 >nul\n")
                        f.write("exit\n")
                    
                    # 创建极简可靠的VBS启动器
                    with open(os.path.join(temp_dir, "silent.vbs"), "w", encoding="utf-8") as f:
                        # 完全不使用变量，直接硬编码批处理路径
                        bat_path_safe = bat_path.replace("\\", "\\\\")
                        f.write('CreateObject("WScript.Shell").Run "' + bat_path_safe + '", 0, False')
                    
                    # 关闭进度窗口
                    progress_window.destroy()
                    
                    # 询问用户是否更新
                    if messagebox.askyesno("文件覆盖确认", 
                                     f"更新将覆盖原有程序文件。\n\n"
                                     f"是否继续更新到版本 v{version}？",
                                     icon=messagebox.WARNING):
                        
                        # 确认开始更新
                        if messagebox.showinfo("更新准备就绪", 
                                        f"已准备好更新到 v{version}。\n\n"
                                        "点击确定后，程序将关闭并自动更新。\n"
                                        "更新完成后，程序会自动重启。\n\n"
                                        "请保存您的工作，然后点击确定继续。"):
                            # 保存设置
                            self.save_menu()
                            
                            # 直接调用wscript.exe
                            subprocess.Popen([
                                "wscript.exe", 
                                os.path.join(temp_dir, "silent.vbs")
                            ], shell=False)
                    else:
                        # 用户取消
                        messagebox.showinfo("更新已取消", "您取消了更新操作。")
                        # 清理临时文件
                        try:
                            import shutil
                            shutil.rmtree(temp_dir, ignore_errors=True)
                        except:
                            pass
                
                except Exception as e:
                    try:
                        progress_window.destroy()
                    except:
                        pass
                    messagebox.showerror("更新失败", f"更新过程中发生错误：{str(e)}")
            
            # 启动下载线程
            import threading
            threading.Thread(target=download_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("更新失败", f"准备更新时发生错误：{str(e)}")

    def add_page(self):
        """添加新页面"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加页面")
        dialog.geometry("250x100")
        dialog.resizable(False, False)
        
        # 设置图标
        icon_path = self.get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            dialog.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window(dialog)
        
        ttk.Label(dialog, text="页面名称:").pack(pady=5)
        entry = ttk.Entry(dialog, width=30)
        entry.pack(pady=5)
        
        def save():
            name = entry.get().strip()
            if name:
                if name in self.pages:
                    messagebox.showwarning("警告", "页面名称已存在！")
                    return
                
                print(f"创建新页面: {name}")
                # 创建新的空菜单
                self.pages[name] = {}
                
                # 在分隔符之前插入新页面
                separator_index = 0
                for i in range(self.page_menu.index("end")):
                    if self.page_menu.type(i) == "separator":
                        separator_index = i
                        break
                
                self.page_menu.insert_command(
                    separator_index,
                    label=name,
                    command=lambda n=name: self.switch_page(n)
                )
                
                # 切换到新页面
                self.current_page = name
                self.menu_items = self.pages[name]
                self.page_button.configure(text=name)
                self.selected_dishes.clear()
                
                # 更新菜单标题
                self.menu_frame.configure(text=name)  # 立即更新标题
                
                # 立即保存配置
                if self.save_menu():
                    print(f"新页面 {name} 保存成功")
                    dialog.destroy()
                    # 更新显示
                    self.update_menu_display()
                    self.update_selected_display()
                else:
                    print(f"新页面 {name} 保存失败")
                    messagebox.showerror("错误", "保存配置失败")
        
        ttk.Button(dialog, text="确定", command=save).pack(pady=5)

    def delete_page(self):
        """删除当前页面"""
        if messagebox.askyesno("确认删除", f"确定要删除页面 {self.current_page} 吗？"):
            # 删除页面数据
            del self.pages[self.current_page]
            
            # 更新菜单项
            menu_items = self.page_menu.index("end")
            for i in range(menu_items + 1):
                try:
                    if self.page_menu.entrycget(i, "label") == self.current_page:
                        self.page_menu.delete(i)
                        # 删除对应的分隔符
                        if i > 0 and self.page_menu.type(i-1) == "separator":
                            self.page_menu.delete(i-1)
                        break
                except:
                    continue
            
            # 切换到默认页面
            self.switch_page("佳佳美食")

    def switch_page(self, page_name):
        """切换到指定页面"""
        self.current_page = page_name
        self.menu_items = self.pages[page_name]
        self.page_button.configure(text=f"{page_name}")
        
        # 更新菜单标题
        self.menu_frame.configure(text=f"{page_name}")  # 只显示页面名称
        
        self.update_menu_display()
        self.selected_dishes.clear()
        self.update_selected_display()
        
        # 在函数末尾添加自动保存
        self.save_menu()

    def update_page_menu(self):
        """更新页面下拉菜单"""
        try:
            # 清空现有菜单项
            self.page_menu.delete(0, 'end')
            
            print("正在更新页面菜单...")
            print(f"当前所有页面: {list(self.pages.keys())}")
            
            # 添加所有页面
            for page_name in self.pages.keys():
                print(f"添加页面到菜单: {page_name}")  # 调试信息
                self.page_menu.add_command(
                    label=page_name,
                    command=lambda n=page_name: self.switch_page(n)
                )
            
            # 添加分隔符和管理选项
            self.page_menu.add_separator()
            self.page_menu.add_command(label="增加页面", command=self.add_page)
            self.page_menu.add_command(label="重命名", command=self.rename_page)
            self.page_menu.add_command(label="删除页面", command=self.delete_page)
            
            print("页面菜单更新完成")
            
        except Exception as e:
            print(f"更新页面菜单时出错: {str(e)}")
            messagebox.showerror("错误", f"更新页面菜单失败：{str(e)}")

    def rename_page(self):
        """重命名当前页面"""
        dialog = tk.Toplevel(self.root)
        dialog.title("重命名页面")
        dialog.geometry("250x100")
        dialog.resizable(False, False)
        
        # 设置图标
        icon_path = self.get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            dialog.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window(dialog)
        
        ttk.Label(dialog, text="新页面名称:").pack(pady=5)
        entry = ttk.Entry(dialog, width=30)
        entry.insert(0, self.current_page)  # 默认显示当前页面名称
        entry.pack(pady=5)
        
        def save():
            new_name = entry.get().strip()
            if new_name:
                if new_name == self.current_page:
                    dialog.destroy()
                    return
                
                if new_name in self.pages:
                    messagebox.showwarning("警告", "页面名称已存在！")
                    return
                
                # 更新页面数据
                self.pages[new_name] = self.pages[self.current_page]
                del self.pages[self.current_page]
                
                # 更新菜单项
                for i in range(self.page_menu.index("end")):
                    try:
                        if self.page_menu.entrycget(i, "label") == self.current_page:
                            self.page_menu.entryconfigure(
                                i,
                                label=new_name,
                                command=lambda n=new_name: self.switch_page(n)
                            )
                            break
                    except:
                        continue
                
                # 更新当前页面名称
                self.current_page = new_name
                self.page_button.configure(text=new_name)
                
                # 保存配置
                self.save_menu()
                
                dialog.destroy()
        
        ttk.Button(dialog, text="确定", command=save).pack(pady=5)

    def show_settings(self):
        """显示帮助菜单"""
        settings_menu = tk.Menu(self.root, tearoff=0)
        settings_menu.add_command(label="概率调整", command=self.show_price_weights)
        settings_menu.add_command(label="反馈问题", command=self.feedback_issue)
        settings_menu.add_command(label="检查更新", command=self.manual_check_updates)
        settings_menu.add_command(label="关于", command=self.show_about)
        
        x = self.settings_button.winfo_rootx()
        y = self.settings_button.winfo_rooty() + self.settings_button.winfo_height()
        settings_menu.post(x, y)

    def feedback_issue(self):
        """显示反馈问题窗口"""
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("反馈问题")
        feedback_window.geometry("400x300")
        feedback_window.resizable(False, False)
        
        # 设置图标
        icon_path = self.get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            feedback_window.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window(feedback_window)
        
        # 创建内容框架
        content_frame = ttk.Frame(feedback_window, padding="20")
        content_frame.pack(fill='both', expand=True)
        
        # 直接添加文本输入框,不使用滚动条
        text_box = tk.Text(
            content_frame,
            wrap=tk.WORD,
            height=10,
            width=40,  # 设置固定宽度
            font=('Microsoft YaHei UI', 10)  # 使用微软雅黑字体
        )
        text_box.pack(fill='both', expand=True)
        
        # 添加提示文本
        text_box.insert('1.0', "请在此处描述您遇到的问题...")
        text_box.bind('<FocusIn>', lambda e: text_box.delete('1.0', tk.END) if text_box.get('1.0', tk.END).strip() == "请在此处描述您遇到的问题..." else None)
        
        # 添加确定按钮
        def submit_feedback():
            feedback_text = text_box.get('1.0', tk.END).strip()
            if feedback_text and feedback_text != "请在此处描述您遇到的问题...":
                #webbrowser.open(f"https://gitee.com/inueue/menu-app/issues/new?issue[title]=用户反馈&issue[description]={feedback_text}")
                feedback_window.destroy()
                messagebox.showinfo("成功", "感谢您的反馈！")
            else:
                messagebox.showwarning("提示", "请输入反馈内容")
        
        ttk.Button(
            content_frame,
            text="确定",
            command=submit_feedback,
            width=10
        ).pack(pady=(20, 0))

    def manual_check_updates(self):
        """手动检查更新"""
        try:
            response = requests.get(
                "https://gitee.com/api/v5/repos/inueue/menu-app/releases/latest",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                latest_version = data["tag_name"].lstrip("v")
                
                if version.parse(latest_version) > version.parse(self.VERSION):
                    # 发现新版本时显示提示
                    if messagebox.askyesno(
                        "发现新版本",
                        f"当前版本：{self.VERSION}\n"
                        f"最新版本：{latest_version}\n\n"
                        "是否前往下载页面更新？"
                    ):
                        webbrowser.open("https://gitee.com/inueue/menu-app/releases")
                else:
                    messagebox.showinfo("检查更新", "当前已是最新版本！")
            else:
                messagebox.showerror("检查更新", "获取版本信息失败，请稍后重试。")
        except Exception as e:
            messagebox.showerror("检查更新", f"检查更新失败：{str(e)}")

    def show_about(self):
        """显示关于窗口"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("300x210")  # 增加高度以容纳图标
        about_window.resizable(False, False)
        
        # 设置图标
        icon_path = self.get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            about_window.iconbitmap(icon_path)
        
        # 居中显示
        self.center_window(about_window)
        
        # 创建内容框架
        content_frame = ttk.Frame(about_window, padding="20")
        content_frame.pack(fill='both', expand=True)
        
        # 添加图标
        try:
            # 尝试加载并显示图标
            from PIL import Image, ImageTk
            icon_size = 64  # 图标大小
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            icon_label = ttk.Label(content_frame, image=icon_photo)
            icon_label.image = icon_photo  # 保持引用防止被垃圾回收
            icon_label.pack(pady=(0, 10))
        except Exception as e:
            print(f"加载图标失败: {str(e)}")
        
        # 使用更好的字体显示标题
        ttk.Label(
            content_frame,
            text="今天吃什么",
            font=('Microsoft YaHei UI', 16, 'bold')
        ).pack(pady=(0, 5))
        
        ttk.Label(
            content_frame,
            text=f"欣仔专用版本 {self.VERSION}",
            foreground='gray'
        ).pack(pady=(0, 5))  # 减小与版权文字的间距
        
        ttk.Label(
            content_frame,
            text="Copyright © 2025 六乙. All Rights Reserved",
            foreground='gray'
        ).pack(pady=(5, 0))  # 减小与版本号的间距

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop() 