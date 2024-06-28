import tkinter as tk
from tkinter import messagebox

from data_management.data_operations import get_data, build_graph, get_line
from pathfinding.shortest_path import calculate_shortest_path, show_path_results
from user_interface.dialogs import add_line_window
from utils.visualization import exit_application, draw_line


global UI_COMPONENTS
UI_COMPONENTS = {}


def setup_main_window(root):
    # 创建画布，用于绘制地铁线路图
    canvas = tk.Canvas(root, width=800, height=300)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 创建一个框架以包含控制按钮
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, fill=tk.X)

    # 获取所有线路名称和ID
    line_options = [(line['lineName'], line['lineID']) for line in get_data()['lines']]
    line_var = tk.StringVar()
    line_var.set('请选择线路')  # 初始提示，不选择任何实际线路

    if line_options:  # 检查列表是否为空
        # 创建带有初始提示的下拉菜单，并包括所有线路名称
        line_menu = tk.OptionMenu(frame, line_var, '请选择线路', *(option[0] for option in line_options))
    else:
        # 如果没有线路，只显示一个默认的无效选项
        line_menu = tk.OptionMenu(frame, line_var, '无可用线路')

    line_menu.pack(side=tk.LEFT, padx=5, pady=5)

    UI_COMPONENTS['line_menu'] = line_menu
    UI_COMPONENTS['line_var'] = line_var

    btn_query_line = tk.Button(frame, text="查询线路", command=lambda: query_line_info(canvas, line_var, line_options))
    btn_query_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 添加线路按钮
    btn_add_line = tk.Button(frame, text="添加线路", command=add_line_window)
    btn_add_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 查询最短路径的按钮
    btn_query_path = tk.Button(frame, text="查询路径",
                               command=lambda: setup_path_query_window(get_data()))
    btn_query_path.pack(side=tk.LEFT, padx=5, pady=5)

    # 退出按钮
    btn_exit = tk.Button(frame, text="退出", command=exit_application)
    btn_exit.pack(side=tk.LEFT, padx=5, pady=5)


def setup_path_query_window(data):
    window = tk.Toplevel()
    window.title("查询最短路径")

    # 创建标签和下拉菜单框架
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)

    # 创建变量和下拉菜单
    start_line_var = tk.StringVar(window)
    start_station_var = tk.StringVar(window)
    end_line_var = tk.StringVar(window)
    end_station_var = tk.StringVar(window)

    # 线路选择下拉菜单
    start_line_menu = tk.OptionMenu(frame, start_line_var, *(line['lineName'] for line in data['lines']))
    start_line_menu.grid(row=0, column=1, padx=10, pady=10)
    end_line_menu = tk.OptionMenu(frame, end_line_var, *(line['lineName'] for line in data['lines']))
    end_line_menu.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(frame, text="起始线路:").grid(row=0, column=0)
    tk.Label(frame, text="目的线路:").grid(row=1, column=0)

    # 站点选择下拉菜单，初始为空
    start_station_menu = tk.OptionMenu(frame, start_station_var, ())
    start_station_menu.grid(row=0, column=3, padx=10, pady=10)
    end_station_menu = tk.OptionMenu(frame, end_station_var, ())
    end_station_menu.grid(row=1, column=3, padx=10, pady=10)

    tk.Label(frame, text="起始站点:").grid(row=0, column=2)
    tk.Label(frame, text="目的站点:").grid(row=1, column=2)

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
        graph = build_graph(data)
        path = calculate_shortest_path(start_station, end_station, graph)
        show_path_results(path, data)
        window.destroy()

    query_button = tk.Button(frame, text="查询路径", command=execute_query)
    query_button.grid(row=2, column=1, columnspan=2, pady=20)

    window.mainloop()


# 根据用户的选择在画布上显示选中的线路信息
def query_line_info(canvas, line_var, line_options):
    """Use the selected line from the dropdown to display on the canvas."""
    line_name = line_var.get()
    line_id = next((line_id for line_name, line_id in line_options if line_name == line_var.get()), None)

    if line_id:
        line = get_line(line_id)
        if line:
            draw_line(canvas, line, get_data())
        else:
            messagebox.showerror("Error", "Line not found.")
    else:
        messagebox.showerror("Error", "Invalid line selection.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Subway Route Management System")
    setup_main_window(root)
    root.mainloop()
