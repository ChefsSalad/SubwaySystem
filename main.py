# main.py
import tkinter as tk
from ui import setup_main_window
import data_management


def on_close(root):
    """Handle window close event by saving data and then destroying the window."""
    data_management.save_data()
    root.destroy()


def main():
    root = tk.Tk()
    root.title("Subway Route Management System")
    data_management.load_data()  # Automatically load data on startup
    setup_main_window(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))  # Set custom close behavior
    root.mainloop()


if __name__ == "__main__":
    main()
