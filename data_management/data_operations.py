from tkinter import messagebox
from .data_io import data, save_data


def add_line(line_id, line_name, stations, time_weights=None):
    if any(line['lineID'] == line_id for line in data['lines']):
        messagebox.showerror("添加错误", f"线路ID {line_id} 已存在。请使用其他ID。")
        return False

    # 确保time_weights的长度等于stations的长度减1
    if time_weights is None:
        time_weights = [1] * (len(stations) - 1)  # 默认权重为1，如果未提供权重

    # 确保权重列表长度正确
    if len(time_weights) != len(stations) - 1:
        messagebox.showerror("添加错误", "时间权重数量必须比站点数量少一个。")
        return False

    # 构建站点列表，包括站点之间的时间权重
    station_objects = []
    for index, name in enumerate(stations):
        station_obj = {
            "stationID": str(index + 1),
            "stationName": name,
            "lineID": line_id,
            "status": "open",
            "nextWeight": time_weights[index] if index < len(time_weights) else None  # 最后一个站点没有下一站，因此为None
        }
        station_objects.append(station_obj)

    new_line = {
        "lineID": line_id,
        "lineName": line_name,
        "stations": station_objects
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
    Build a graph representation of the subway network considering station closures and time weights.
    :param data: The data dictionary containing all lines, stations, and transfers with weights
    :return: A dictionary representing the graph of the network, where keys are station names, and values are dicts of neighboring stations with weights.
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
                graph[station['stationName']] = {}

            if previous_station and previous_station['status'] == 'open':  # 确保前一个站点是开放的
                # 使用时间权重连接前一个站点和当前站点
                weight = station.get('nextWeight', None)  # 获取权重，如果没有指定则默认为None或其他适当的默认值
                if weight is not None:  # 仅当有有效的权重时添加连接
                    graph[previous_station['stationName']][station['stationName']] = weight
                    graph[station['stationName']][previous_station['stationName']] = weight
            previous_station = station  # 更新前一个站点为下次迭代准备

    # 处理换乘，确保涉及的站点都是开放的，并添加权重
    for transfer in data['transfers']:
        from_station_info = next((s for l in data['lines'] for s in l['stations'] if s['stationName'] == transfer['fromStation'] and s['lineID'] == transfer['fromLine']), None)
        to_station_info = next((s for l in data['lines'] for s in l['stations'] if s['stationName'] == transfer['toStation'] and s['lineID'] == transfer['toLine']), None)
        if from_station_info and to_station_info and from_station_info['status'] == 'open' and to_station_info['status'] == 'open':
            weight = transfer.get('nextWeight', None)  # 获取换乘的权重
            if weight is not None:  # 确保权重有效
                graph[from_station_info['stationName']][to_station_info['stationName']] = weight
                graph[to_station_info['stationName']][from_station_info['stationName']] = weight

    return graph


def get_data():
    return data
