import json
import os
from tkinter import messagebox  # 用于错误提示

data_directory = 'data'
data_filename = 'data.json'
data_path = os.path.join(os.path.dirname(__file__), '..', data_directory, data_filename)

data = {
    "lines": [],
    "transfers": []
}


def load_data():
    global data
    if not os.path.exists(data_path):
        save_data()  # 如果文件不存在，则创建一个新文件
    else:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)


def save_data():
    global data
    os.makedirs(os.path.dirname(data_path), exist_ok=True)  # 确保目录存在
    # 在保存前按线路ID排序
    data['lines'].sort(key=lambda line: int(line['lineID']))
    with open(data_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        # messagebox.showinfo("保存数据", "数据已成功保存！")


load_data()
