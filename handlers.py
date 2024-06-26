# handlers.py
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox, simpledialog
import re  # 导入正则表达式库
import data_management
import utils
from utils import draw_line


def load_data(canvas):
    """Load data from a JSON file and update the canvas. Check if data is non-empty before drawing."""
    data = data_management.load_data()
    if data:
        if data['lines']:  # Check if there is at least one line
            draw_line(canvas, data['lines'][0])  # Draw the first line for simplicity
        else:
            messagebox.showinfo("Load Data", "No subway lines found in the data file.")
    else:
        messagebox.showerror("Load Data", "Failed to load data. Please check the data file.")


def save_data():
    """Save the current data back to the JSON file."""
    data_management.save_data()


def add_line_window():
    """Open a new window to input details for a new subway line, ensuring all fields are required."""
    window = Toplevel()
    window.title("添加新线路")

    Label(window, text="线路ID:").pack()
    line_id_entry = Entry(window)
    line_id_entry.pack()

    Label(window, text="线路名称:").pack()
    line_name_entry = Entry(window)
    line_name_entry.pack()

    Label(window, text="站点（使用逗号分隔）:").pack()
    stations_entry = Entry(window)
    stations_entry.pack()

    submit_btn = Button(window, text="提交", command=lambda: submit_new_line(
        line_id_entry.get(), line_name_entry.get(), stations_entry.get(), window))
    submit_btn.pack()


def submit_new_line(line_id, line_name, stations, window):
    """Handle the submission of a new line, ensuring no fields are empty."""
    if not line_id.strip() or not line_name.strip() or not stations.strip():
        # 如果任何一个输入为空，显示错误信息
        messagebox.showerror("输入错误", "所有字段均为必填项，请确保填写所有信息。")
        return

    stations_list = re.split(r'[ ,，]+', stations.strip())
    if not stations_list:
        messagebox.showerror("输入错误", "至少需要一个站点。")
        return

    success = data_management.add_line(line_id, line_name, stations_list)
    if success:
        window.destroy()
        data_management.save_data()  # 添加成功后保存数据
        messagebox.showinfo("成功", "新线路添加成功，并已保存数据。")
    else:
        # 如果添加失败（例如ID重复），保留窗口开启，允许用户更正
        pass


def query_line_info(canvas):
    """Prompt user for a line ID and display the line on the canvas if found."""
    line_id = simpledialog.askstring("Query Line", "Enter the line ID:")
    line = data_management.get_line(line_id)
    if line:
        utils.draw_line(canvas, line, data_management.data)  # Pass the entire data if needed
    else:
        messagebox.showerror("Error", "Line not found.")


def exit_application():
    """Exit the application."""
    import sys
    sys.exit(0)
