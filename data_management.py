# data_management.py
import json
import os
from tkinter import messagebox  # 用于错误提示

data_path = 'data.json'
data = {
    "lines": [],
    "transfers": []
}


def load_data():
    global data
    if not os.path.exists(data_path):
        save_data()  # Create a new file if it doesn't exist
    else:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)


def save_data():
    with open(data_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_data():
    return data  # Returns the entire data dictionary


def add_line(line_id, line_name, stations):
    """Add a new subway line to the data dictionary if the line ID is not already taken."""
    if any(line['lineID'] == line_id for line in data['lines']):
        # 如果找到重复的ID，显示错误消息并不执行添加操作
        messagebox.showerror("添加错误", f"线路ID {line_id} 已存在。请使用其他ID。")
        return False
    new_line = {
        "lineID": line_id,
        "lineName": line_name,
        "stations": [{"stationID": str(index + 1), "stationName": name} for index, name in enumerate(stations)]
    }
    data['lines'].append(new_line)
    return True


def get_line(line_id):
    """Retrieve a line by its ID from the data."""
    print(f"Looking for line ID: {line_id}")
    for line in data['lines']:
        print(f"Checking line: {line['lineID']}")
        if line['lineID'] == str(line_id):
            return line
    return None
