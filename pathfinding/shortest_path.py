from collections import deque
import tkinter as tk
from tkinter import messagebox


# 执行最短路径计算
def calculate_shortest_path(start, end, graph):
    """
    Uses Breadth-First Search (BFS) to find the shortest path between two stations in a subway network.
    :param start: Starting station name.
    :param end: Ending station name.
    :param graph: Graph of the subway system where keys are station names and values are sets of connected stations.
    :return: List of stations representing the shortest path, or None if no path exists.
    """
    if start not in graph or end not in graph:
        return None

    queue = deque([(start, [start])])  # Queue of tuples (current_station, path_to_station)
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == end:
            return path

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


# 显示路径查询结果
def show_path_results(path, data):
    """
    Formats and displays the result of a path search, considering transfers and closed stations.
    :param path: List of station names forming the path from start to end.
    :param data: Subway data containing station status and transfer information.
    """
    if not path:
        result = "不可到达。"
    else:
        result = ""
        previous_line = None
        for i in range(len(path) - 1):
            current_station = path[i]
            next_station = path[i + 1]

            # Determine the line of the current connection
            current_line = None
            for line in data['lines']:
                if any(s['stationName'] == current_station for s in line['stations']) and any(
                        s['stationName'] == next_station for s in line['stations']):
                    current_line = line['lineName']
                    break

            if previous_line is None or previous_line != current_line:
                if result:
                    result += f"\n{current_line} 线 {current_station} 上，"
                else:
                    result += f"乘坐 {current_line} 线 {current_station} 上车，"

            if i == len(path) - 2:
                result += f"{next_station} 下车"

            previous_line = current_line

    tk.messagebox.showinfo("查询结果", result)