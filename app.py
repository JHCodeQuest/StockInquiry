import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
import easyocr
import sqlite3
import os
import imagehash
from PIL import Image as PILImage

#Load inventory
inventory = pd.read_csv("inventory_data.csv")

#set up OCR reader
reader = easyocr.Reader(['en'], gpu=False)

#Create history DB if it doesn't exist
conn = sqlite3.connect('history.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS search_history
             (id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, part_number TEXT, result TEXT)''')
conn.commit()

# Compare images using hash similarity
def compare_images(img1_path, img2_path):
    hash1 = imagehash.average_hash(PILImage.open(img1_path))
    hash2 = imagehash.average_hash(PILImage.open(img2_path))
    return 1 - (hash1 - hash2) / len(hash1.hash)**2

#Try to find item
def identify_item(image_path):
    results = []
    
    #OCR detection
    ocr_result = reader.readtext(image_path, detail=0)
    ocr_text = " ".join(ocr_result).lower()
    
    #Compare with reference images
    for _, row in inventory.iterrows():
        print("CSV Columns:", inventory.columns)
        similarity = compare_images(image_path, row["image_path"])
        if similarity > 0.7 or row["part_number"].lower() in ocr_text or row["item_name"].lower() in ocr_text:
            results.append((row["item_name"], row["part_number"], row["location"], row["stock_qty"], round(similarity, 2)))
        
        results.sort(key=lambda x: x[-1], reverse=True)
        return results

# GUI setup
root = tk.Tk()
root.title("Stock Inquiry Assistant")
root.geometry("600x800")

label = tk.Label(root, text="Upload Item Image", font=("Arial", 14))
label.pack(pady=10)

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpe")])
    if not file_path:
        return
    
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(150, 150, image=photo)
    canvas.image = photo
    
    results = identify_item(file_path)
    if results:
        result_box.delete(*result_box.get_children())
        for item in results[:5]:
            result_box.insert("", "end", values=item[:-1])
            #save top match to history
            c.execute("INSERT INTO search_history (item_name, part_number, result) VALUES (?, ?, ?)", (item[0], item[1], "Match"))
            conn.commit()
    else:
        messagebox.showinfo("No match", "No matching item found.")
        c.execute("INSERT INTO search_history (item_name, part_number, result) VALUES (?, ?, ?)", ("Unknown", "Unknown", "No match"))
        conn.commit()

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=5)

columns = ("Item Name", "Part Number", "Location", "Stock Qty")
result_box = ttk.Treeview(root, columns=columns, show="headings", height=5)
for col in columns:
    result_box.heading(col, text=col)
result_box.pack(pady=10)

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Search History")
    tk.Label(history_window, text="Search History", font=("Arial", 12, "bold")).pack(pady=5)
    
    hist_table = ttk.Treeview(history_window, columns=("Item", "Part", "Result"), show="headings", height=10)
    for col in ("Item", "Part", "Result"):
        hist_table.heading(col, text=col)
    hist_table.pack()
    
    c.execute("SELECT item_name, part_number, result FROM search_history ORDER BY id DESC LIMIT 20")
    for row in c.fetchall():
        hist_table.insert("", "end", values=row)

tk.Button(root, text="View History", command=show_history).pack(pady=5)

root.mainloop()