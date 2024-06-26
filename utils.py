# utils.py
import tkinter as tk

import tkinter as tk


def draw_line(canvas, line, data):
    """
    Draw the subway line on the canvas, wrapping into S-shape if it extends beyond the canvas width.
    Highlight transfer stations and correctly draw lines between stations.
    """
    if not line:
        return

    canvas.delete("all")  # Clear the canvas for new drawing

    start_x, start_y = 50, 50  # Initial starting position on the canvas
    x, y = start_x, start_y
    step_x, step_y = 100, 50  # Distance between stations horizontally and vertically
    max_x = canvas.winfo_width() - 100  # Maximum x position before wrapping, adjusted to avoid edge overflow
    direction = 1  # Direction of x movement, 1 for right, -1 for left
    last_x, last_y = x, y  # Track the last station's position for line drawing

    for i, station in enumerate(line['stations']):
        # Check if this station is a transfer station
        is_transfer = any(t['fromStation'] == station['stationName'] or t['toStation'] == station['stationName'] for t in data['transfers'])

        # Draw station as a circle, use a different color if it's a transfer station
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red" if is_transfer else "blue", outline="black")
        canvas.create_text(x, y + 20, text=station['stationName'])

        # Draw line from last station to this one, starting from the second station
        if i > 0:
            canvas.create_line(last_x, last_y, x, y, fill="gray")

        # Update last_x and last_y to current station's position for the next iteration
        last_x, last_y = x, y

        # Calculate next station's x and y
        next_x = x + direction * step_x
        if next_x > max_x or next_x < start_x:
            # If next x is out of bounds, wrap to next line and reverse direction
            y += step_y
            direction *= -1  # Change direction
            x += direction * step_x  # Adjust x considering the new direction
        else:
            x = next_x  # Continue in the same direction

        # Add a click event to show transfer information if it is a transfer station
        if is_transfer:
            canvas.tag_bind("station_{}".format(i), "<Button-1>", lambda event, s=station: show_transfers(canvas, s, data))

def show_transfers(canvas, station, data):
    """
    Show transfer details for the clicked station.
    """
    transfers = [t for t in data['transfers'] if t['fromStation'] == station['stationName'] or t['toStation'] == station['stationName']]
    transfer_info = "Transfers for " + station['stationName'] + ":\n" + "\n".join(f"{t['fromLine']} to {t['toLine']} at {t['toStation'] if t['fromStation'] == station['stationName'] else t['fromStation']}" for t in transfers)
    tk.messagebox.showinfo("Transfer Info", transfer_info)



def calculate_shortest_path(start, end, graph):
    """
    Use BFS to find the shortest path between two stations in the subway network.
    :param start: The name of the start station
    :param end: The name of the end station
    :param graph: The graph dictionary representing subway network
    :return: A list of station names representing the shortest path
    """
    from collections import deque
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        visited.add(current)
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None


def build_graph(data):
    """
    Build a graph representation of the subway network.
    :param data: The data dictionary containing all lines and transfers
    :return: A dictionary representing the graph of the network
    """
    graph = {}
    for line in data['lines']:
        previous_station = None
        for station in line['stations']:
            if station['stationName'] not in graph:
                graph[station['stationName']] = set()
            if previous_station:
                graph[previous_station].add(station['stationName'])
                graph[station['stationName']].add(previous_station)
            previous_station = station['stationName']
    for transfer in data['transfers']:
        if transfer['fromStation'] in graph and transfer['toStation'] in graph:
            graph[transfer['fromStation']].add(transfer['toStation'])
            graph[transfer['toStation']].add(transfer['fromStation'])
    return graph
