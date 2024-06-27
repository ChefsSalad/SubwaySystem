# utils.py
import tkinter as tk
from tkinter import simpledialog, Toplevel, Radiobutton, Label, Entry, Button

import data_management
import utils
from handlers import add_neighboring_station, delete_station, view_transfers


def on_right_click(event, station, canvas, data, line_id):
    # 创建一个简单的右键菜单
    menu = tk.Menu(canvas, tearoff=0)
    menu.add_command(label="增加邻近站点", command=lambda: add_neighboring_station(station, data, canvas, line_id))
    menu.add_command(label="删除该站点", command=lambda: delete_station(station, data, canvas, line_id))
    menu.add_command(label="查看换乘情况", command=lambda: view_transfers(station, data, canvas))  # 新增查看换乘情况

    # 显示菜单
    menu.post(event.x_root, event.y_root)

def update_canvas_on_select(event, canvas, data, line_id):
    # 当选中列表中的项时，重新绘制相关线路
    line = data_management.get_line(line_id)
    if line:
        utils.draw_line(canvas, line, data)


def draw_line(canvas, line, data):
    """
    Draw the subway line on the canvas, wrapping into S-shape if it extends beyond the canvas width.
    Highlight transfer stations and correctly draw lines between stations.
    """
    if not line:
        return

    canvas.delete("all")  # Clear the canvas for new drawing

    # Display the line name at the top of the canvas
    canvas.create_text(400, 20, text=f"当前线路：{line['lineName']}", font=('Helvetica', 10, 'bold'))


    start_x, start_y = 50, 50  # Initial starting position on the canvas
    x, y = start_x, start_y
    step_x, step_y = 100, 50  # Distance between stations horizontally and vertically
    max_x = canvas.winfo_width() - 100  # Maximum x position before wrapping, adjusted to avoid edge overflow
    direction = 1  # Direction of x movement, 1 for right, -1 for left
    last_x, last_y = x, y  # Track the last station's position for line drawing

    for i, station in enumerate(line['stations']):
        # Check if this station is a transfer station
        is_transfer = any(
            t['fromStation'] == station['stationName'] or t['toStation'] == station['stationName'] for t in
            data['transfers'])

        # Draw station as a circle, use a different color if it's a transfer station
        station_id = "station_{}".format(station['stationName'])  # 使用站点名称作为唯一标识

        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red" if is_transfer else "blue", outline="black",
                           tags=(station_id,))
        canvas.create_text(x, y + 20, text=station['stationName'])
        canvas.tag_bind(station_id, "<Button-3>",
                        lambda event, s=station: on_right_click(event, s, canvas, data, line['lineID']))

        # Draw line from last station to this one, starting from the second station
        if i > 0:
            canvas.create_line(last_x, last_y, x, y, fill="gray")

        # Update last_x and last_y to current station's position for the next iteration
        last_x, last_y = x, y

        # Calculate next station's x and y
        next_x = x + direction * step_x
        if next_x > max_x or next_x < start_x:
            # If next x is out of bounds, wrap to next line and reverse direction
            y += step_y
            direction *= -1  # Change direction
            x += direction * step_x  # Adjust x considering the new direction
        else:
            x = next_x  # Continue in the same direction

        # Add a click event to show transfer information if it is a transfer station
        if is_transfer:
            canvas.tag_bind("station_{}".format(i), "<Button-1>",
                            lambda event, s=station: show_transfers(canvas, s, data))


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
