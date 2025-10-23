#Thinking/loading screen
import tkinter as tk
import threading
import time

def show_loading(parent, task_function):
    loading = tk.Toplevel(parent)
    loading.title("Processing...")
    loading.geometry("300x150")
    
    label = tk.Label(
        loading,
        text="Thinking... Please wait.",
        font=("Arial", 12)
    )
    label.pack(pady=30)
    
    
    def run_task():
        time.sleep(0.3) #allow ui to draw
        task_function()
        loading.destroy()

    threading.Thread(target=run_task).start()