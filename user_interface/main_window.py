import tkinter as tk
from tkinter import messagebox

from data_management.data_operations import get_data, build_graph, get_line
from interaction_handlers.command_functions import update_line_dropdown
from pathfinding.shortest_path import show_path_results, calculate_shortest_time_path, \
    calculate_least_transfers_path
from user_interface.dialogs import add_line_window
from utils.visualization import exit_application, draw_line


def setup_main_window(root):
    canvas = tk.Canvas(root, width=800, height=300)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, fill=tk.X)

    line_var = tk.StringVar(value='请选择线路')
    # 注意：初始化下拉菜单时先不添加任何实际选项
    line_menu = tk.OptionMenu(frame, line_var, '请选择线路')
    line_menu.pack(side=tk.LEFT, padx=5, pady=5)

    # 确保所有必要的 UI 组件已经创建并存储后，再更新下拉菜单
    update_line_dropdown(line_menu, line_var)  # 更新下拉菜单

    btn_query_line = tk.Button(frame, text="查询线路", command=lambda: query_line_info(canvas, line_var, line_menu))
    btn_query_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 添加线路按钮
    btn_add_line = tk.Button(frame, text="添加线路", command=lambda: add_line_window(line_menu, line_var))
    btn_add_line.pack(side=tk.LEFT, padx=5, pady=5)

    # 新增查询最短时间路径按钮
    btn_query_shortest_time = tk.Button(frame, text="查询最短路径",
                                        command=lambda: setup_path_query_window(get_data()))
    btn_query_shortest_time.pack(side=tk.LEFT, padx=5, pady=5)

    btn_exit = tk.Button(frame, text="退出", command=exit_application)
    btn_exit.pack(side=tk.LEFT, padx=5, pady=5)


def setup_path_query_window(data):
    window = tk.Toplevel()
    window.title("查询路径选项")

    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)

    # 创建变量和下拉菜单
    start_line_var = tk.StringVar(window)
    start_station_var = tk.StringVar(window)
    end_line_var = tk.StringVar(window)
    end_station_var = tk.StringVar(window)
    query_type_var = tk.StringVar(window, value='最短时间')

    # 线路选择下拉菜单
    start_line_menu = tk.OptionMenu(frame, start_line_var, *(line['lineName'] for line in data['lines']))
    start_line_menu.grid(row=0, column=1, padx=10, pady=10)
    end_line_menu = tk.OptionMenu(frame, end_line_var, *(line['lineName'] for line in data['lines']))
    end_line_menu.grid(row=1, column=1, padx=10, pady=10)

    # 站点选择下拉菜单，初始为空
    start_station_menu = tk.OptionMenu(frame, start_station_var, "选择起始站")
    start_station_menu.grid(row=0, column=3, padx=10, pady=10)
    end_station_menu = tk.OptionMenu(frame, end_station_var, "选择目的站")
    end_station_menu.grid(row=1, column=3, padx=10, pady=10)

    # 查询类型选择下拉菜单
    query_type_menu = tk.OptionMenu(frame, query_type_var, '最短时间', '最少换乘')
    query_type_menu.grid(row=2, column=1, padx=10, pady=10)

    # 更新站点下拉菜单的函数
    def update_station_menu(line_var, station_var, station_menu):
        selected_line = next((line for line in data['lines'] if line['lineName'] == line_var.get()), None)
        station_var.set('')
        menu = station_menu["menu"]
        menu.delete(0, 'end')
        for station in selected_line['stations']:
            menu.add_command(label=station['stationName'], command=lambda value=station['stationName']: station_var.set(value))

    # 绑定更新函数到线路变量
    start_line_var.trace('w', lambda *args: update_station_menu(start_line_var, start_station_var, start_station_menu))
    end_line_var.trace('w', lambda *args: update_station_menu(end_line_var, end_station_var, end_station_menu))

    # 查询按钮
    def execute_query():
        start_station = start_station_var.get()
        end_station = end_station_var.get()
        query_type = query_type_var.get()  # 确保有一个变量来获取查询类型
        graph = build_graph(data)

        if query_type == '最短时间':
            path, total_time, transfers = calculate_shortest_time_path(start_station, end_station, graph)
        else:
            path, total_time, transfers = calculate_least_transfers_path(start_station, end_station, graph)

        show_path_results(path, total_time, data)  # 调整函数调用以传递额外的参数
        window.destroy()

    query_button = tk.Button(frame, text="transfers", command=execute_query)
    query_button.grid(row=3, column=1, columnspan=2, pady=20)

    window.mainloop()


# 根据用户的选择在画布上显示选中的线路信息
def query_line_info(canvas, line_var, line_menu):
    try:
        # 获取下拉菜单的当前选项
        selected_line_name = line_var.get()
        print(f"Selected Line Name: {selected_line_name}")  # 调试输出选中的线路名称

        # 获取所有线路选项（假设这些选项是在 setup_main_window 中设置的）
        line_options = [(line['lineName'], line['lineID']) for line in get_data()['lines']]
        print(f"Line Options: {line_options}")  # 调试输出所有线路选项

        # 根据选中的线路名称查找对应的线路 ID
        line_id = next((line_id for line_name, line_id in line_options if line_name == selected_line_name), None)
        print(f"Line ID: {line_id}")  # 调试输出找到的线路 ID

        if line_id is not None:
            # 如果找到了线路 ID，继续处理（例如绘制线路图）
            line = get_line(line_id)
            if line:
                draw_line(canvas, line, get_data(), line_menu, line_var)
            else:
                messagebox.showerror("Error", "Line not found.")
        else:
            messagebox.showerror("Error", "Invalid line selection.")
    except Exception as e:
        # 错误处理
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Subway Route Management System")
    setup_main_window(root)
    root.mainloop()
