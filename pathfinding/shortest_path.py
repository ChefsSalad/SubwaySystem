from collections import deque
import tkinter as tk
from tkinter import messagebox
import json
# 执行最短路径计算
import heapq

# def calculate_shortest_time_path(start, end, graph):
#     if start not in graph or end not in graph:
#         return None, 0
#
#     queue = [(0, start, [start])]
#     visited = {}
#     while queue:
#         current_time, current, path = heapq.heappop(queue)
#
#         if current in visited and visited[current] <= current_time:
#             continue
#         visited[current] = current_time
#
#         if current == end:
#             transfers = sum(1 for i in range(len(path) - 1) if path[i].split('_')[0] != path[i + 1].split('_')[0])
#             return path, current_time, transfers
#
#         for neighbor, time in graph[current].items():
#             if neighbor not in visited or visited[neighbor] > current_time + time:
#                 print(path + [neighbor])
#                 print(current_time + time)
#                 heapq.heappush(queue, (current_time + time, neighbor, path + [neighbor]))
#
#     return None, 0, 0


# def calculate_least_transfers_path(start, end, graph):
#     if start not in graph or end not in graph:
#         return None, 0, 0
#
#     path=[]
#
#
#     queue = deque([(start, [start])])
#     visited = {}
#     while queue:
#         current, path = queue.popleft()
#
#         if current in visited:
#             continue
#         visited[current] = path
#
#         if current == end:
#             total_time = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
#             transfers = sum(1 for i in range(len(path) - 1) if path[i].split('_')[0] != path[i + 1].split('_')[0])
#             return path, total_time, transfers
#
#         for neighbor in graph[current]:
#             if neighbor not in visited:
#                 queue.append((neighbor, path + [neighbor]))
#
#     return None, 0, 0

import heapq

# def calculate_shortest_time_path(start, end, graph):
#     if start not in graph or end not in graph:
#         return None, 0, 0
#
#     shortest_path = None
#     shortest_time = float('inf')
#     shortest_transfers = 0
#
#     queue = [(0, start, [start])]
#     while queue:
#         current_time, current, path = heapq.heappop(queue)
#         print(heapq)
#
#         if current == end:
#             transfers = sum(1 for i in range(len(path) - 1) if path[i].split('_')[0] != path[i + 1].split('_')[0])
#             if current_time < shortest_time:
#                 shortest_path = path
#                 shortest_time = current_time
#                 shortest_transfers = transfers
#
#             continue
#
#         for neighbor, time in graph[current].items():
#             new_time = current_time + time
#             heapq.heappush(queue, (new_time, neighbor, path + [neighbor]))
#
#     if shortest_path:
#         return shortest_path, shortest_time, shortest_transfers
#     else:
#         return None, 0, 0


from collections import deque





def calculate_shortest_time_path(start, end, graph):
    #print(graph)
    if start not in graph or end not in graph:
        return None, 0, 0

    queue = deque([(start, [start], 0)])
    visited = set()

    best_path = None
    best_time = float('inf')

    while queue:
        current, path, total_time = queue.popleft()

        if current in visited:
            continue
        visited.add(current)

        if current == end:

            if total_time < best_time:
                best_path = path
                best_time = total_time
            continue

        for neighbor in graph[current]:
            #if neighbor not in visited:
                travel_time = graph[current][neighbor]
                queue.append((neighbor, path + [neighbor], total_time + travel_time))

    if best_path is None:
        return None, 0, 0

    min_transfers = len(best_path) - 2  # 计算换乘次数（经过的站点数减去起点和终点）
    print(best_path)
    print(best_time)
    print(min_transfers)
    return best_path, best_time, min_transfers

from collections import deque

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
    total_time = sum(graph[best_path[i]][best_path[i + 1]] for i in range(len(best_path) - 1))
    return best_path,total_time, len(best_path) - 1


# def calculate_least_transfers_path(start, end, graph):
#     if start not in graph or end not in graph:
#         return None, 0, 0
#     # print(start)
#     # print(graph)
#     # 队列初始化，包含起点、路径和当前换乘次数
#     queue = deque([(start, [start], 0)])
#     visited = set()
#
#     min_transfers = float('inf')
#     best_path = None
#     best_time = float('inf')
#
#     while queue:
#         current, path, transfers = queue.popleft()
#         #print(current)
#         if current in visited:
#             continue
#         visited.add(current)
#
#         if current == end:
#             total_time = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
#             if transfers < min_transfers:
#                 min_transfers = transfers
#                 best_path = path
#                 best_time = total_time
#             elif transfers == min_transfers and total_time < best_time:
#                 best_path = path
#                 best_time = total_time
#             continue
#
#         for neighbor in graph[current]:
#             if neighbor not in visited:
#                 #print(neighbor)
#                 next_transfers = transfers + (1 if current.split('_')[0] != neighbor.split('_')[0] else 0)
#                 # print(path + [neighbor])
#                 queue.append((neighbor, path + [neighbor], next_transfers))
#
#     if best_path is None:
#         return None, 0, 0
#     return best_path, best_time, min_transfers


def show_path_results(path, total_time, data):
    if not path:
        result = "不可到达。"
    else:
        result = "路线详情：\n"
        previous_line = None
        station_count = 0  # 用于计数经过的站点
        details = []  # 用于存储路线的详细信息
        transfers = 0  # 用于计数换乘次数

        for i in range(len(path) - 1):
            current_station = path[i]
            next_station = path[i + 1]
            # 查找当前站点和下一站点所在的线路名称
            current_line = next((line['lineName'] for line in data['lines'] if
                                 any(s['stationName'] == current_station for s in line['stations']) and
                                 any(s['stationName'] == next_station for s in line['stations'])), None)
            if previous_line is None:
                # 初始化时设置起始站和线路信息
                previous_line = current_line
                details.append(f"从 {current_station} (乘坐 {current_line} ) 出发，")
                station_count = 1
            elif previous_line == current_line:
                station_count += 1  # 同一条线路上，累加站点数量
            else:
                # 当换乘到不同的线路时，记录前一条线路的信息
                details.append(f"经过 {station_count} 站在 {current_station} 换乘至 {current_line}")
                station_count = 1  # 重置站点计数器
                transfers += 1  # 增加换乘次数
                previous_line = current_line

        # 添加最后一条线路的信息
        details.append(f"经过 {station_count} 站在 {path[-1]} 下车。")

        result += " ".join(details) + f"\n总时间: {total_time} 分钟\n换乘次数: {transfers}"

    tk.messagebox.showinfo("查询结果", result)
