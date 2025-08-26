import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import pymongo

# Get the correct path
BASE_DIR = os.path.dirname(__file__)

# MongoDB setup for delete functionality
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["live_weather_db"]
collection = db["live_weather_data"]

# Function to delete all data
def delete_data():
    result = messagebox.askyesno("Confirm", "Are you sure you want to delete all weather data?")
    if result:
        collection.delete_many({})
        messagebox.showinfo("Deleted", "All weather data deleted from MongoDB.")

# Functions to start other processes
def start_fetching():
    script_path = os.path.join(BASE_DIR, "live_mausam_fetch1.py")
    subprocess.Popen(['python', script_path])
    messagebox.showinfo("Info", "Live weather data fetching started!")

def start_analysis():
    script_path = os.path.join(BASE_DIR, "live_mausam_analysis1.py")
    subprocess.Popen(['python', script_path])
    messagebox.showinfo("Info", "Live data analysis started!")

def start_prediction():
    script_path = os.path.join(BASE_DIR, "live_mausam_ai1.py")
    subprocess.Popen(['python', script_path])
    messagebox.showinfo("Info", "AI-based prediction started!")

def start_visualization():
    script_path = os.path.join(BASE_DIR, "live_mausam_visualization1.py")
    subprocess.Popen(['python', script_path])
    messagebox.showinfo("Info", "Visualization started!")

# Create main GUI window
root = tk.Tk()
root.title("Live Weather Dashboard")
root.geometry("600x500")

# Load and set background
bg_img = Image.open(os.path.join(BASE_DIR, "weather_background.png"))
bg_img = bg_img.resize((600, 500), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load and place weather icon
icon_img = Image.open(os.path.join(BASE_DIR, "weather_icon.png"))
icon_img = icon_img.resize((80, 80), Image.LANCZOS)
icon_photo = ImageTk.PhotoImage(icon_img)
icon_label = tk.Label(root, image=icon_photo, bg='#dfe6e9')
icon_label.place(x=10, y=10)

# Decorative button styles
button_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#0984e3",
    "fg": "white",
    "padx": 12,
    "pady": 8,
    "bd": 0,
    "relief": tk.RAISED,
    "activebackground": "#74b9ff"
}

# Buttons
fetch_button = tk.Button(root, text="Start Live Data Fetching", command=start_fetching, **button_style)
analyze_button = tk.Button(root, text="Start Live Data Analysis", command=start_analysis, **button_style)
predict_button = tk.Button(root, text="Start AI Prediction", command=start_prediction, **button_style)
visual_button = tk.Button(root, text="Start Visualization", command=start_visualization, **button_style)
delete_button = tk.Button(root, text="Delete All Weather Data", command=delete_data, bg="#d63031", fg="white", font=("Arial", 12, "bold"), padx=12, pady=8, bd=0)

# Place buttons
fetch_button.place(x=180, y=120, width=250)
analyze_button.place(x=180, y=180, width=250)
predict_button.place(x=180, y=240, width=250)
visual_button.place(x=180, y=300, width=250)
delete_button.place(x=180, y=360, width=250)

# Start GUI loop
root.mainloop()
