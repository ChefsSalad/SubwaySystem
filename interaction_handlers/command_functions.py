from data_management.data_operations import add_line, save_data, get_line, get_data
from utils.visualization import draw_line
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox, StringVar, OptionMenu
import re  # 导入正则表达式库


# 添加邻近站点
def add_neighboring_station(station, data, canvas, line_id):
    def submit():
        new_station_name = entry.get()
        position = var.get()
        # 确保输入不为空
        if not new_station_name.strip():
            tk.messagebox.showerror("错误", "站点名称不能为空")
            return

        current_line = next((line for line in data['lines'] if line['lineID'] == line_id), None)

        # 检查是否存在同名站点
        if any(st['stationName'] == new_station_name for st in current_line['stations']):
            tk.messagebox.showerror("错误", "当前线路中已存在同名站点，请使用其他名称。")
            return

        # 找到当前站点在data中的位置，并根据选择插入新站点
        for line in data['lines']:
            for idx, st in enumerate(line['stations']):
                if st['stationName'] == station['stationName']:
                    if position == 'prev':
                        line['stations'].insert(idx, {"stationID": str(idx), "stationName": new_station_name,
                                                      "lineID": line_id, "status": "open"})
                    else:
                        line['stations'].insert(idx + 1, {"stationID": str(idx + 1), "stationName": new_station_name,
                                                          "lineID": line_id, "status": "open"})
                    break
        # 更新站点ID
        for line in data['lines']:
            for idx, st in enumerate(line['stations']):
                st['stationID'] = str(idx)
        # 保存数据
        save_data()
        window.destroy()

        # 更新数据后重新绘制线路
        line = get_line(line_id)
        if line:
            draw_line(canvas, line, data)

    window = Toplevel()
    window.title("增加邻近站点")

    var = tk.StringVar(value="next")
    tk.Radiobutton(window, text="增加上一站", variable=var, value="prev").pack()
    tk.Radiobutton(window, text="增加下一站", variable=var, value="next").pack()

    Label(window, text="站点名称:").pack()
    entry = Entry(window)
    entry.pack()

    Button(window, text="提交", command=submit).pack()


# 删除站点
def delete_station(station, data, canvas, line_id):
    response = tk.messagebox.askyesno("确认删除", f"您确定要删除站点{station['stationName']}吗？")
    if response:
        # 从data中找到并删除站点
        for line in data['lines']:
            # 过滤掉要删除的站点
            new_stations = [st for st in line['stations'] if st['stationName'] != station['stationName']]
            # 如果新站点列表为空，则删除整条线路
            if not new_stations:
                data['lines'].remove(line)
                tk.messagebox.showinfo("线路删除", f"已删除整条线路：{line['lineName']}，因为没有其他站点。")
            else:
                line['stations'] = new_stations
                # 更新站点ID
                for idx, st in enumerate(line['stations']):
                    st['stationID'] = str(idx + 1)

        # 删除与该站点相关的所有换乘关系
        data['transfers'] = [t for t in data['transfers'] if
                             t['fromStation'] != station['stationName'] and t['toStation'] != station['stationName']]

        # 保存数据
        save_data()
        messagebox.showinfo("删除成功", "站点已删除，并更新了数据。")

        # 更新数据后重新绘制线路
        line = get_line(line_id)
        if line:
            draw_line(canvas, line, data)
        else:
            canvas.delete("all")  # 如果线路被删除，则清空 Canvas
            update_line_dropdown(line_menu, data)


# 开放关闭站点
def toggle_station_status(station, data, canvas, line_id, new_status):
    # 更改指定站点的状态
    station['status'] = new_status

    # 找到与此站点有直接换乘关系的所有站点，并更改它们的状态
    for transfer in data['transfers']:
        if transfer['fromStation'] == station['stationName'] and transfer['fromLine'] == line_id:
            # 找到换乘到的站点，并更新状态
            to_station_info = next((s for l in data['lines'] for s in l['stations'] if
                                    s['stationName'] == transfer['toStation'] and s['lineID'] == transfer['toLine']),
                                   None)
            if to_station_info:
                to_station_info['status'] = new_status
        elif transfer['toStation'] == station['stationName'] and transfer['toLine'] == line_id:
            # 找到从哪个站点换乘过来的，并更新状态
            from_station_info = next((s for l in data['lines'] for s in l['stations'] if
                                      s['stationName'] == transfer['fromStation'] and s['lineID'] == transfer[
                                          'fromLine']), None)
            if from_station_info:
                from_station_info['status'] = new_status

    # 保存数据
    save_data()

    # 重新绘制线路图以显示状态更新
    line = get_line(line_id)
    if line:
        draw_line(canvas, line, data)


# 添加换乘站点
def add_transfer(station, data, canvas, listbox):
    line_id = station['lineID']  # 直接从站点数据中获取 lineID
    transfer_window = tk.Toplevel()
    transfer_window.title("添加换乘站")

    main_frame = tk.Frame(transfer_window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 下拉菜单选择线路，排除当前站点所在的线路
    line_var = tk.StringVar(transfer_window)
    line_options = [line['lineName'] for line in data['lines'] if line['lineID'] != line_id]
    if line_options:  # 确保至少有一个选项可用
        line_menu = tk.OptionMenu(main_frame, line_var, *line_options)
    else:
        line_menu = tk.OptionMenu(main_frame, line_var, "无可用线路")
    line_menu.pack()

    # 下拉菜单选择站点，初始化为空
    station_var = tk.StringVar(transfer_window)
    station_menu = tk.OptionMenu(main_frame, station_var, "选择站点")
    station_menu.pack()

    # 更新站点菜单的函数
    def update_station_menu(*args):
        selected_line = next((line for line in data['lines'] if line['lineName'] == line_var.get()), None)
        if selected_line:
            station_options = [st['stationName'] for st in selected_line['stations']]
            station_menu['menu'].delete(0, 'end')
            for station_name in station_options:
                station_menu['menu'].add_command(label=station_name, command=tk._setit(station_var, station_name))
        else:
            station_menu['menu'].delete(0, 'end')
            station_menu['menu'].add_command(label="无站点", command=tk._setit(station_var, "无站点"))

    line_var.trace('w', update_station_menu)  # 当选中的线路变化时更新站点选项

    def confirm_transfer():
        to_line = next((line for line in data['lines'] if line['lineName'] == line_var.get()), None)
        if to_line and not any(
                t['fromStation'] == station['stationName'] and t['toStation'] == station_var.get() for t in
                data['transfers']):
            new_transfer = {
                "fromLine": line_id,
                "fromStation": station['stationName'],
                "toLine": to_line['lineID'],
                "toStation": station_var.get()
            }
            data['transfers'].append(new_transfer)
            save_data()
            listbox.insert(tk.END,
                           f"{new_transfer['fromLine']} 线 {new_transfer['fromStation']} 到 {new_transfer['toLine']} 线 {new_transfer['toStation']}")
            transfer_window.destroy()
            # 刷新画布以显示更新
            line = get_line(line_id)
            if line:
                draw_line(canvas, line, data)

    confirm_button = tk.Button(transfer_window, text="确定", command=confirm_transfer)
    confirm_button.pack()


# 删除换乘站点
def delete_transfer(transfers, listbox, data, canvas, line_id):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        transfer = transfers[index]
        confirm = tk.messagebox.askyesno("确认删除",
                                         f"确认删除从 {transfer['fromLine']} 线 {transfer['fromStation']} 换乘到 {transfer['toLine']} 线 {transfer['toStation']} 的换乘关系及其反向关系吗？")
        if confirm:
            # 删除当前换乘及其反向换乘
            data['transfers'] = [t for t in data['transfers'] if not (
                    (t['fromStation'] == transfer['fromStation'] and t['toStation'] == transfer['toStation']) or
                    (t['fromStation'] == transfer['toStation'] and t['toStation'] == transfer['fromStation'])
            )]
            save_data()
            listbox.delete(index)  # 删除列表中的项
            tk.messagebox.showinfo("删除成功", "换乘关系已删除")

            # 更新数据后重新绘制线路
            line = get_line(line_id)
            if line:
                draw_line(canvas, line, data)
            else:
                canvas.delete("all")  # 如果线路被删除，则清空 Canvas


# 处理添加新线路
def submit_new_line(line_id, line_name, stations, window):
    from user_interface.main_window import UI_COMPONENTS
    line_menu = UI_COMPONENTS.get('line_menu')
    line_var = UI_COMPONENTS.get('line_var')

    if line_menu is not None:
        update_line_dropdown(line_menu, line_var)
    else:
        messagebox.showerror("错误", "线路菜单未正确初始化。")

    if not line_id.strip() or not line_name.strip() or not stations.strip():
        messagebox.showerror("输入错误", "所有字段均为必填项，请确保填写所有信息。")
        return

    stations_list = re.split(r'[ ,，]+', stations.strip())
    success = add_line(line_id, line_name, stations_list)
    if success:
        window.destroy()
        save_data()  # 添加成功后保存数据
        messagebox.showinfo("成功", "新线路添加成功。")
        update_line_dropdown(line_menu, line_var)  # 更新下拉列表
    else:
        # 如果添加失败（例如ID重复），保留窗口开启，允许用户更正
        pass


# 更新下拉框
def update_line_dropdown(line_menu, data):
    from user_interface.main_window import UI_COMPONENTS

    line_menu = UI_COMPONENTS.get('line_menu')
    line_var = UI_COMPONENTS.get('line_var')

    try:
        menu = line_menu['menu']
        menu.delete(0, 'end')  # 删除旧的菜单项
        line_options = [line['lineName'] for line in data['lines']]
        for option in line_options:
            menu.add_command(label=option, command=lambda value=option: line_menu.setvar(value))
        if line_options:
            line_menu.setvar(line_options[0])  # 默认选择第一个线路
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update line dropdown: {e}")
