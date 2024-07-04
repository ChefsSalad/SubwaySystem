from tkinter import messagebox
from data_management.data_io import data, save_data
import json
from collections import deque
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


# def calculate_least_transfers_path(start, end, graph):
#
#     # 假设 data.json 是你的 JSON 文件
#     with open(r'D:\download\SubwaySystem\data\data.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     if start not in graph or end not in graph:
#         return None, 0, 0
#
#     queue = deque([(start, [start], 0)])
#     visited = set()
#
#     best_path = None
#     least_transfers = float('inf')
#
#     while queue:
#         current, path, transfers = queue.popleft()
#         #print(path)
#         # if current == '小南门':
#         #     print(path)
#         # if current in visited:
#         #     continue
#         visited.add(current)
#         print(path)
#         if current == end:
#             #print(path)
#             previous_line = -1
#             for i in range(len(path) - 1):
#                 current_station = path[i]
#                 next_station = path[i + 1]
#                 current_line = next((line['lineName'] for line in data['lines'] if
#                                      any(s['stationName'] == current_station for s in line['stations']) and
#                                      any(s['stationName'] == next_station for s in line['stations'])), None)
#
#                 if previous_line ==-1:
#                     previous_line = current_line
#                     station_count = 1
#                 elif previous_line == current_line:
#                     station_count += 1
#                 else:
#
#                     station_count = 1
#                     transfers += 1
#                     previous_line = current_line
#
#             if transfers < least_transfers:
#                 best_path = path
#                 least_transfers = transfers
#             continue
#
#         for neighbor in graph[current]:
#             if (path[-1] =='马当路'):
#                 print(graph[current])
#                 print(neighbor)
#
#             if (len(path)>1 and path[-2] == '马当路'):
#             # if (path[-1] == '陆家浜路' ):
#                 print(path)
#                 print(path[-2])
#                 print(graph[current])
#             #neighbors=
#             #if neighbor not in visited:
#                 #print(neighbor)
#             # if neighbor=='小南门':
#             #    print(path)
#
#             queue.append((neighbor, path + [neighbor], transfers + 1))
#             if (path[-1] == '马当路'):
#                  print('---------------------------------------------------------\n已经加入：', path + [neighbor])
#                  print(queue[-1])
#
#
#     if best_path is None:
#          return None, 0, 0
#
#     return best_path, len(best_path) - 2, least_transfers


# def calculate_least_transfers_path(start, end, graph):
#     # Load the subway system data from JSON file
#     with open(r'D:\download\SubwaySystem\data\data.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     # Check if start or end stations are not in the graph
#     if start not in graph or end not in graph:
#         return None, 0, 0
#
#     # Initialize the queue with the starting station, path, and transfer count
#     queue = deque([(start, [start], 0)])
#     visited = set()
#
#     best_path = None
#     least_transfers = float('inf')
#
#     while queue:
#         current, path, transfers = queue.popleft()
#
#         # If the current station is the destination
#         if current == end:
#             previous_line = -1
#             current_transfers = 0
#             for i in range(len(path) - 1):
#                 current_station = path[i]
#                 next_station = path[i + 1]
#                 current_line = next((line['lineName'] for line in data['lines'] if
#                                      any(s['stationName'] == current_station for s in line['stations']) and
#                                      any(s['stationName'] == next_station for s in line['stations'])), None)
#
#                 if previous_line == -1:
#                     previous_line = current_line
#                 elif previous_line != current_line:
#                     current_transfers += 1
#                     previous_line = current_line
#
#             if current_transfers < least_transfers:
#                 best_path = path
#                 least_transfers = current_transfers
#             continue
#
#         for neighbor in graph[current]:
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 queue.append((neighbor, path + [neighbor], transfers))
#
#     if best_path is None:
#         return None, 0, 0
#
#     return best_path, len(best_path) - 1, least_transfers

import json

def calculate_least_transfers_path(start, end, graph):
    # Load the subway system data from JSON file
    with open(r'D:\download\SubwaySystem\data\data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if start or end stations are not in the graph
    if start not in graph or end not in graph:
        return None, 0, 0

    # Initialize variables
    least_transfers = float('inf')
    best_path = []
    visited = set()

    # Depth-first search function
    def dfs(current, path, transfers):
        nonlocal least_transfers, best_path

        # If reached the end station, calculate transfers
        if current == end:
            current_transfers = 0
            previous_line = -1
            for i in range(len(path) - 1):
                current_station = path[i]
                next_station = path[i + 1]
                current_line = next((line['lineName'] for line in data['lines'] if
                                     any(s['stationName'] == current_station for s in line['stations']) and
                                     any(s['stationName'] == next_station for s in line['stations'])), None)

                if previous_line == -1:
                    previous_line = current_line
                elif previous_line != current_line:
                    current_transfers += 1
                    previous_line = current_line

            if current_transfers < least_transfers:
                best_path = path[:]
                least_transfers = current_transfers
            return

        # Visit neighbors
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, transfers)
                path.pop()
                visited.remove(neighbor)

    # Start DFS from the start station
    visited.add(start)
    dfs(start, [start], 0)

    return best_path, least_transfers, len(best_path) - 1


graph = build_graph(data)

print(calculate_least_transfers_path('松江大学城', '小南门', graph))