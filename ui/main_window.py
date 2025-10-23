#GUI layout and navigation

import tkinter as tk
from tkinter import ttk
from ui.loading_screen import show_loading
from features.inventory_tools import process_inventory_data
from features.camera_capture import identify_item_from_camera

def launch_app():
    root = tk.Tk()
    root.title("Stock helper")
    root.geometry("500x400")
    
    ttk.Label(root, text="Stock Helper", font=("Arial", 16)).pack(pady=20)
    
    ttk.Button(
        root,
        text="Take Photo",
        command=lambda: show_loading(root, identify_item_from_camera)
    ).pack(pady=10)
    
    ttk.Button(root, text="Quit", command=root.destroy).pack(pady=10)
    
    root.mainloop()