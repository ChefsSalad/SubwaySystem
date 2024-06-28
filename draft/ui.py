# ui.py
import tkinter as tk
from tkinter import Toplevel, Label, Button, OptionMenu, StringVar

import utils
from draft.handlers import add_line_window, query_line_info, exit_application
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

    # 获取所有线路名称和ID
    line_options = [(line['lineName'], line['lineID']) for line in data_management.get_data()['lines']]
    line_var = tk.StringVar()
    line_var.set(line_options[0][0])  # 默认选择第一个线路

    # 下拉菜单选择线路
    line_menu = tk.OptionMenu(frame, line_var, *[option[0] for option in line_options])
    line_menu.pack(side=tk.LEFT, padx=5, pady=5)

    btn_query_line = tk.Button(frame, text="查询线路", command=lambda: query_line_info(canvas, line_var, line_options))
    btn_query_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 添加线路按钮
    btn_add_line = tk.Button(frame, text="添加线路", command=add_line_window)
    btn_add_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 查询最短路径的按钮
    btn_query_path = tk.Button(frame, text="查询路径",
                               command=lambda: setup_path_query_window(data_management.get_data()))
    btn_query_path.pack(side=tk.LEFT, padx=5, pady=5)

    # 退出按钮
    btn_exit = tk.Button(frame, text="退出", command=exit_application)
    btn_exit.pack(side=tk.LEFT, padx=5, pady=5)


def setup_path_query_window(data):
    window = Toplevel()
    window.title("查询最短路径")

    # 创建标签和下拉菜单框架
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)

    # 创建变量和下拉菜单
    start_line_var = StringVar(window)
    start_station_var = StringVar(window)
    end_line_var = StringVar(window)
    end_station_var = StringVar(window)

    # 线路选择下拉菜单
    start_line_menu = OptionMenu(frame, start_line_var, *(line['lineName'] for line in data['lines']))
    start_line_menu.grid(row=0, column=1, padx=10, pady=10)
    end_line_menu = OptionMenu(frame, end_line_var, *(line['lineName'] for line in data['lines']))
    end_line_menu.grid(row=1, column=1, padx=10, pady=10)

    Label(frame, text="起始线路:").grid(row=0, column=0)
    Label(frame, text="目的线路:").grid(row=1, column=0)

    # 站点选择下拉菜单，初始为空
    start_station_menu = OptionMenu(frame, start_station_var, ())
    start_station_menu.grid(row=0, column=3, padx=10, pady=10)
    end_station_menu = OptionMenu(frame, end_station_var, ())
    end_station_menu.grid(row=1, column=3, padx=10, pady=10)

    Label(frame, text="起始站点:").grid(row=0, column=2)
    Label(frame, text="目的站点:").grid(row=1, column=2)

    # 更新站点下拉菜单的函数
    def update_station_menu(line_var, station_var, station_menu):
        selected_line = next(line for line in data['lines'] if line['lineName'] == line_var.get())
        station_var.set('')
        menu = station_menu["menu"]
        menu.delete(0, 'end')
        for station in selected_line['stations']:
            menu.add_command(label=station['stationName'],
                             command=lambda value=station['stationName']: station_var.set(value))

    # 绑定更新函数到线路变量
    start_line_var.trace('w', lambda *args: update_station_menu(start_line_var, start_station_var, start_station_menu))
    end_line_var.trace('w', lambda *args: update_station_menu(end_line_var, end_station_var, end_station_menu))

    # 查询按钮
    def execute_query():
        start_station = start_station_var.get()
        end_station = end_station_var.get()
        graph = data_management.build_graph(data)
        path = utils.calculate_shortest_path(start_station, end_station, graph)
        utils.show_path_results(path, data)
        window.destroy()

    query_button = Button(frame, text="查询路径", command=execute_query)
    query_button.grid(row=2, column=1, columnspan=2, pady=20)

    window.mainloop()
