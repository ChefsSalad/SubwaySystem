from collections import deque
import tkinter as tk
from tkinter import messagebox

# 执行最短路径计算
import heapq


def calculate_shortest_time_path(start, end, graph):
    if start not in graph or end not in graph:
        return None, 0

    queue = [(0, start, [start])]
    visited = {}
    while queue:
        current_time, current, path = heapq.heappop(queue)

        if current in visited and visited[current] <= current_time:
            continue
        visited[current] = current_time

        if current == end:
            transfers = sum(1 for i in range(len(path) - 1) if path[i].split('_')[0] != path[i + 1].split('_')[0])
            return path, current_time, transfers

        for neighbor, time in graph[current].items():
            if neighbor not in visited or visited[neighbor] > current_time + time:
                heapq.heappush(queue, (current_time + time, neighbor, path + [neighbor]))

    return None, 0, 0


def calculate_least_transfers_path(start, end, graph):
    if start not in graph or end not in graph:
        return None, 0, 0

    queue = deque([(start, [start])])
    visited = {}
    while queue:
        current, path = queue.popleft()

        if current in visited:
            continue
        visited[current] = path

        if current == end:
            total_time = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
            transfers = sum(1 for i in range(len(path) - 1) if path[i].split('_')[0] != path[i + 1].split('_')[0])
            return path, total_time, transfers

        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None, 0, 0


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
