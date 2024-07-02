import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button

from data_management.data_io import data
from data_management.data_operations import get_line
from interaction_handlers.command_functions import submit_new_line, delete_transfer, add_transfer
from utils.visualization import draw_line


# 创建添加新线路的窗口，包括输入字段和提交按钮
def add_line_window(line_menu, line_var):
    window = Toplevel()
    window.title("添加新线路")


    Label(window, text="线路ID:").pack()
    line_id_entry = Entry(window)
    line_id_entry.pack()

    Label(window, text="线路名称:").pack()
    line_name_entry = Entry(window)
    line_name_entry.pack()

    Label(window, text="站点（使用空格分隔）:").pack()
    stations_entry = Entry(window)
    stations_entry.pack()

    # 确保传递 line_menu 和 line_var 到提交函数
    submit_btn = Button(window, text="提交", command=lambda: submit_new_line(
        line_id_entry.get(), line_name_entry.get(), stations_entry.get(), window, line_menu, line_var))
    submit_btn.pack()


# 展示一个站点的换乘情况
def view_transfers(station, data, canvas, line_menu, line_var):
    window = tk.Toplevel()
    window.title(f"换乘情况 - {station['stationName']}")

    window.geometry('300x200')

    # 筛选以当前站点为起点的换乘关系，并按照目的线路ID和目的站点名称排序
    transfers = [t for t in data['transfers'] if
                 t['fromStation'] == station['stationName'] and t['fromLine'] == station['lineID']]
    transfers.sort(key=lambda x: (x['toLine'], x['toStation']))  # 根据目的线路ID和站点名称排序

    listbox = tk.Listbox(window)
    for t in transfers:
        listbox.insert(tk.END, f" {t['fromLine']} ： {t['fromStation']} -> {t['toLine']} ： {t['toStation']} —— {t['nextWeight']}")
    listbox.pack(fill=tk.BOTH, expand=True)

    # 删除和添加换乘站的按钮
    delete_button = tk.Button(window, text="删除该换乘站",
                              command=lambda: delete_transfer(transfers, listbox, data, canvas, station['lineID'], line_menu, line_var))
    delete_button.pack(side=tk.LEFT)
    add_button = tk.Button(window, text="添加换乘站", command=lambda: add_transfer(station, data, canvas, listbox, line_menu, line_var))
    add_button.pack(side=tk.RIGHT)

    # 这里还需要确保更新画布后显示正确的线路
    listbox.bind('<<ListboxSelect>>',
                 lambda event: update_canvas_on_select(event, canvas, data, station['lineID'], line_menu, line_var))


# 重新刷新地铁路线图
def update_canvas_on_select(event, canvas, data, line_id, line_menu, line_var):
    # 当选中列表中的项时，重新绘制相关线路
    line = get_line(line_id)
    if line:
        draw_line(canvas, line, data, line_menu, line_var)


# 展示换乘站点的信息
def show_transfers(canvas, station, data):
    """
    Show transfer details for the clicked station.
    """
    transfers = [t for t in data['transfers'] if
                 t['fromStation'] == station['stationName'] or t['toStation'] == station['stationName']]
    transfer_info = "Transfers for " + station['stationName'] + ":\n" + "\n".join(
        f"{t['fromLine']} to {t['toLine']} at {t['toStation'] if t['fromStation'] == station['stationName'] else t['fromStation']}"
        for t in transfers)
    tk.messagebox.showinfo("Transfer Info", transfer_info)
