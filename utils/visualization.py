import tkinter as tk
from interaction_handlers.event_handlers import on_right_click


# 绘制路线图
def draw_line(canvas, line, data, line_menu, line_var):
    if not line:
        return

    canvas.delete("all")  # 清空画布准备新的绘图

    # 显示线路名称在画布顶部
    canvas.create_text(400, 20, text=f"当前线路：{line['lineName']}", font=('Helvetica', 10, 'bold'))

    start_x, start_y = 50, 50  # 初始化起始位置
    x, y = start_x, start_y
    step_x, step_y = 100, 50  # 站点间水平和垂直的距离
    max_x = canvas.winfo_width() - 100  # 避免溢出画布的最大x位置
    direction = 1  # x方向移动，1向右，-1向左

    for i, station in enumerate(line['stations']):
        # 判断是否为换乘站
        is_transfer = any(t['fromStation'] == station['stationName'] or t['toStation'] == station['stationName'] for t in data['transfers'])

        # 绘制站点为一个圆形，如果是换乘站则用不同颜色
        station_id = f"station_{station['stationName']}"
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red" if is_transfer else "blue", outline="black", tags=(station_id,))
        canvas.create_text(x, y + 20, text=station['stationName'])
        canvas.tag_bind(station_id, "<Button-3>",
                        lambda event, s=station: on_right_click(event, s, canvas, data, line['lineID'], line_menu,
                                                                line_var))

        # 如果站点状态是封闭的，则绘制叉号
        if station.get('status') == 'closed':
            canvas.create_line(x - 12, y - 12, x + 12, y + 12, fill="black", width=2)
            canvas.create_line(x + 12, y - 12, x - 12, y + 12, fill="black", width=2)

        # 如果存在下一个站点且当前站点有权重，则绘制连线和显示权重
        if i < len(line['stations']) - 1 and 'nextWeight' in station:
            next_station = line['stations'][i + 1]
            canvas.create_line(x, y, x + direction * step_x, y, fill="gray")
            mid_x, mid_y = x + direction * step_x / 2, y
            canvas.create_text(mid_x, mid_y, text=str(station['nextWeight']), fill="black", font=('Helvetica', 10))

        # 计算下一个站点的x和y位置
        next_x = x + direction * step_x
        if next_x > max_x or next_x < start_x:
            # 如果下一个x位置超出界限，则换行并反转方向
            y += step_y
            direction *= -1
            x += direction * step_x
        else:
            x = next_x  # 继续同方向移动


# 退出界面
def exit_application():
    """Exit the application."""
    import sys
    sys.exit(0)
