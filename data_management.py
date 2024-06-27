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
    return data


def add_line(line_id, line_name, stations):
    if any(line['lineID'] == line_id for line in data['lines']):
        messagebox.showerror("添加错误", f"线路ID {line_id} 已存在。请使用其他ID。")
        return False
    new_line = {
        "lineID": line_id,
        "lineName": line_name,
        "stations": [{"stationID": str(index + 1), "stationName": name, "lineID": line_id} for index, name in
                     enumerate(stations)]
    }
    data['lines'].append(new_line)
    return True


def get_line(line_id):
    for line in data['lines']:
        if line['lineID'] == str(line_id):
            return line
    return None
