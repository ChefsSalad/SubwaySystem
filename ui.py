# ui.py
import tkinter as tk
from tkinter import simpledialog, messagebox

import utils
from handlers import add_line_window, query_line_info, exit_application
import data_management

def setup_main_window(root):
    """
    Setup the main window with a canvas for drawing subway lines and buttons for various actions.
    """
    # 创建画布，用于绘制地铁线路图
    canvas = tk.Canvas(root, width=800, height=300)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 创建一个框架以包含控制按钮
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, fill=tk.X)

    # 添加线路按钮
    btn_add_line = tk.Button(frame, text="添加线路", command=add_line_window)
    btn_add_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 查询线路按钮
    btn_query_line = tk.Button(frame, text="查询线路", command=lambda: query_line_info(canvas))
    btn_query_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 退出按钮
    btn_exit = tk.Button(frame, text="退出", command=exit_application)
    btn_exit.pack(side=tk.LEFT, padx=5, pady=5)
