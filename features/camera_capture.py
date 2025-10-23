import cv2
import os
import datetime
from tkinter import Toplevel, Label, Button, messagebox
from PIL import Image, ImageTk

def take_photo(root, identify_item, db_cursor, db_conn):
    """ Opens the webcam, or phone camera. allows the user to take a photo,
    save it, run the item in the identification process.
    """
    cap = cv2.VideoCapture(1) # for mac 1 is iphone cam, 2 is webcam
    
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Camera is not accessible")
        return
    
    #create camera preview window
    preview = Toplevel(root)
    preview.title("Camera Preview")
    preview.geometry("300x250")
    preview.configure(bg="white")
    
    Label(preview, text="Camera Preview", fg="white", bg="#222", font=("Arial", 14)).pack(pady=5)
    video_label = Label(preview, bg="#222")
    video_label.pack()
    
    running = True
    captured_image = None
    
    def update_frame():
        """continuously update the webcam preview"""
        if not running:
            return
        
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (400, 200))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        
        if preview.winfo_exists():
            preview.after(30, update_frame)
    
    def capture_photo():
        """Capture a still image and process it"""
        nonlocal captured_image, running
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Capture Error", "Failed to capture image")
            return
        
        #save the captured image
        os.makedirs("captured_images", exist_ok=True)
        filename = datetime.datetime.now().strftime("captured_images/photo_%Y%m%d_%H%M%S.jpg")
        cv2.imwrite(filename, frame)
        messagebox.showinfo("Saved", f"Photo saved as:\n{filename}")  
        
        #show thinking popup
        thinking_popup = Toplevel(preview)
        thinking_popup.title("Processing")
        Label(thinking_popup, text="Identifying item...", font=("Arial", 14), padx=20, pady=20).pack()
        thinking_popup.update()
        
        #stop the camera and close the preview
        running = False
        cap.release()
        preview.destroy()
        
        #identify the item
        try:
            results = identify_item(filename)
        except Exception as e:
            messagebox.showerror("Error", f"Identification failed: {e}")
            thinking_popup.destroy()
            return
        
        thinking_popup.destroy()
        
        #handle the results
        if results:
            result_text = "\n".join(
                f"{item[0]} ({item[1]}) - Location: {item[2]}, Stock: {item[3]}"
                for item in results
            )
            messagebox.showinfo("Identification Results", result_text)

            # Save best result to DB
            top_result = results[0]
            db_cursor.execute(
                "INSERT INTO search_history (item_name, part_number, result, time) VALUES (?, ?, ?, datetime('now'))",
                (top_result[0], top_result[1], "Match")
            )
            db_conn.commit()
        else:
            messagebox.showinfo("No Match Found", "No matching item found.")
            db_cursor.execute(
                "INSERT INTO search_history (item_name, part_number, result, time) VALUES (?, ?, ?, datetime('now'))",
                ("Unknown", "Unknown", "No match")
            )
            db_conn.commit()
        
    def close_camera():
        """Stops webcam and closes the preview."""
        nonlocal running
        running = False
        cap.release()
        preview.destroy()

    # Buttons
    Button(preview, text="Take Photo", command=capture_photo, width=15, bg="#4CAF50", fg="white").pack(side="left", padx=10, pady=10)
    Button(preview, text="Cancel", command=close_camera, width=15, bg="#f44336", fg="white").pack(side="right", padx=10, pady=10)

    # Start live video feed
    update_frame()