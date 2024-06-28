import tkinter as tk

def on_right_click(event, station, canvas, data, line_id, line_menu, line_var):

    from interaction_handlers.command_functions import add_neighboring_station, delete_station, toggle_station_status
    from user_interface.dialogs import view_transfers

    # 创建一个简单的右键菜单
    menu = tk.Menu(canvas, tearoff=0)
    menu.add_command(label="增加邻近站点", command=lambda: add_neighboring_station(station, data, canvas, line_id, line_menu, line_var))
    menu.add_command(label="删除该站点", command=lambda: delete_station(station, data, canvas, line_id, line_menu, line_var))
    menu.add_command(label="查看换乘情况", command=lambda: view_transfers(station, data, canvas, line_menu, line_var))  # 新增查看换乘情况
    if station.get('status') == 'open':
        menu.add_command(label="封闭站点",
                         command=lambda: toggle_station_status(station, data, canvas, line_id, 'closed'))
    else:
        menu.add_command(label="恢复站点",
                         command=lambda: toggle_station_status(station, data, canvas, line_id, 'open'))
    menu.post(event.x_root, event.y_root)
