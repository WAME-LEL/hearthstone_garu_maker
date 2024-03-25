import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import time
import keyboard

# Global list to store coordinates and flag to control the automation loop
coordinates = [(None, None)] * 4
running = False

def update_coordinates_display():
    coordinates_list_var.set([f"Coordinate {i + 1}: {coord}" for i, coord in enumerate(coordinates)])

def capture_coordinate(index):
    x, y = pyautogui.position()
    coordinates[index] = (x, y)
    update_coordinates_display()

def setup_keyboard_listeners():
    for i in range(4):
        keyboard.add_hotkey(f'F{i+2}', lambda i=i: capture_coordinate(i))

    keyboard.add_hotkey('F6', start_automation)
    keyboard.add_hotkey('F7', stop_automation)

def automate_clicks():
    global running
    running = True
    while running:
        for i, (x, y) in enumerate(coordinates):
            if not running:
                break
            if x is None or y is None:
                continue
            if i == 0:  # The first click is a right-click.
                pyautogui.rightClick(x, y)
            else:
                pyautogui.click(x, y)
            time.sleep(1 if i < 2 else 4 if i == 2 else 2)

def start_automation():
    global running
    if not running:
        if all(coord != (None, None) for coord in coordinates):  # Ensure all coordinates are set.
            threading.Thread(target=automate_clicks, daemon=True).start()
        else:
            messagebox.showwarning("Warning", "Please capture all coordinates before starting.")
    else:
        messagebox.showinfo("Info", "Automation is already running.")

def stop_automation():
    global running
    running = False
    messagebox.showinfo("Info", "Automation stopped.")

def exit_program():
    global running
    running = False
    root.quit()

# GUI setup
root = tk.Tk()
root.title("Automation Setup")
root.geometry('400x200')

coordinates_list_var = tk.StringVar(value=["Coordinate 1: (None, None)", "Coordinate 2: (None, None)", "Coordinate 3: (None, None)", "Coordinate 4: (None, None)"])
coordinates_listbox = tk.Listbox(root, listvariable=coordinates_list_var, width=50, height=4)
coordinates_listbox.pack(pady=20)

setup_keyboard_listeners()

root.protocol("WM_DELETE_WINDOW", exit_program)  # Ensure clean exit on window close
root.mainloop()
