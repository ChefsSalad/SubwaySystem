import tkinter as tk
from interaction_handlers.event_handlers import on_right_click


# 绘制路线图
def draw_line(canvas, line, data, line_menu, line_var):
    from user_interface.dialogs import show_transfers

    if not line:
        return

    canvas.delete("all")  # Clear the canvas for new drawing

    # Display the line name at the top of the canvas
    canvas.create_text(400, 20, text=f"当前线路：{line['lineName']}", font=('Helvetica', 10, 'bold'))

    start_x, start_y = 50, 50  # Initial starting position on the canvas
    x, y = start_x, start_y
    step_x, step_y = 100, 50  # Distance between stations horizontally and vertically
    max_x = canvas.winfo_width() - 100  # Maximum x position before wrapping, adjusted to avoid edge overflow
    direction = 1  # Direction of x movement, 1 for right, -1 for left
    last_x, last_y = x, y  # Track the last station's position for line drawing

    for i, station in enumerate(line['stations']):
        # Check if this station is a transfer station
        is_transfer = any(
            t['fromStation'] == station['stationName'] or t['toStation'] == station['stationName'] for t in
            data['transfers'])

        # Draw station as a circle, use a different color if it's a transfer station
        station_id = "station_{}".format(station['stationName'])  # 使用站点名称作为唯一标识

        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red" if is_transfer else "blue", outline="black",
                           tags=(station_id,))
        canvas.create_text(x, y + 20, text=station['stationName'])
        canvas.tag_bind(station_id, "<Button-3>",
                        lambda event, s=station: on_right_click(event, s, canvas, data, line['lineID'], line_menu, line_var))

        # 修改叉号样式：更粗的线条和红色
        cross_thickness = 2  # 线条粗细
        cross_color = "black"  # 叉号颜色

        if station.get('status') == 'closed':
            canvas.create_line(x - 12, y - 12, x + 12, y + 12, fill=cross_color, width=cross_thickness)
            canvas.create_line(x + 12, y - 12, x - 12, y + 12, fill=cross_color, width=cross_thickness)

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
            canvas.tag_bind("station_{}".format(i), "<Button-1>",
                            lambda event, s=station: show_transfers(canvas, s, data))


# 退出界面
def exit_application():
    """Exit the application."""
    import sys
    sys.exit(0)
