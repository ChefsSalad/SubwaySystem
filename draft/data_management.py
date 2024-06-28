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
        save_data()  # 如果文件不存在，则创建一个新文件
    else:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)


def save_data():
    global data
    # 在保存前按线路ID排序
    data['lines'].sort(key=lambda line: int(line['lineID']))
    with open(data_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        # messagebox.showinfo("保存数据", "数据已成功保存！")

def get_data():
    return data


def add_line(line_id, line_name, stations):
    if any(line['lineID'] == line_id for line in data['lines']):
        messagebox.showerror("添加错误", f"线路ID {line_id} 已存在。请使用其他ID。")
        return False
    new_line = {
        "lineID": line_id,
        "lineName": line_name,
        "stations": [{"stationID": str(index + 1), "stationName": name, "lineID": line_id, "status": "open"} for
                     index, name in
                     enumerate(stations)]
    }
    data['lines'].append(new_line)
    return True


def get_line(line_id):
    for line in data['lines']:
        if line['lineID'] == str(line_id):
            return line
    return None


def build_graph(data):
    """
    Build a graph representation of the subway network considering station closures.
    :param data: The data dictionary containing all lines and transfers
    :return: A dictionary representing the graph of the network
    """
    graph = {}
    # 首先处理线路内的站点
    for line in data['lines']:
        previous_station = None
        for station in line['stations']:
            if station['status'] == 'closed':
                previous_station = None  # 当前站点封闭，断开与前一个站点的连接
                continue
            if station['stationName'] not in graph:
                graph[station['stationName']] = set()
            if previous_station and previous_station['status'] == 'open':  # 确保前一个站点是开放的
                # 连接前一个站点和当前站点，因为两者都是开放的
                graph[previous_station['stationName']].add(station['stationName'])
                graph[station['stationName']].add(previous_station['stationName'])
            previous_station = station  # 更新前一个站点为下次迭代准备

    # 处理换乘，确保涉及的站点都是开放的
    for transfer in data['transfers']:
        from_station_info = next((s for l in data['lines'] for s in l['stations'] if s['stationName'] == transfer['fromStation'] and s['lineID'] == transfer['fromLine']), None)
        to_station_info = next((s for l in data['lines'] for s in l['stations'] if s['stationName'] == transfer['toStation'] and s['lineID'] == transfer['toLine']), None)
        if from_station_info and to_station_info and from_station_info['status'] == 'open' and to_station_info['status'] == 'open':
            graph[from_station_info['stationName']].add(to_station_info['stationName'])
            graph[to_station_info['stationName']].add(from_station_info['stationName'])

    return graph




