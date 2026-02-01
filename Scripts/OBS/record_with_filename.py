import obspython as obs
import os
import tkinter as tk
from tkinter import font
import threading
import time
import re

# --- GLOBAL SETTINGS ---
recording_path = ""
rename_delay = 1.0

def script_description():
    return "<b>Pop-up Renamer (Total Rename)</b><br/>Replaces the entire filename after recording stops.<br/>Includes duplicate protection."

def script_properties():
    props = obs.obs_properties_create()
    
    obs.obs_properties_add_path(
        props,
        "recording_path",
        "Recording Path (Must match OBS Output)",
        obs.OBS_PATH_DIRECTORY,
        None,
        None
    )
    
    obs.obs_properties_add_float(
        props,
        "rename_delay",
        "Safety Delay (seconds)",
        0.1, 10.0, 0.1
    )
    
    return props

def script_update(settings):
    global recording_path, rename_delay
    recording_path = obs.obs_data_get_string(settings, "recording_path")
    rename_delay = obs.obs_data_get_double(settings, "rename_delay")

def sanitize_filename(name):
    """Removes illegal characters"""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def find_newest_fresh_video():
    if not recording_path or not os.path.exists(recording_path):
        print("Rename Script: Path not valid.")
        return None

    files = []
    extensions = ('.mkv', '.mp4', '.mov', '.flv', '.ts')
    
    for f in os.listdir(recording_path):
        if f.lower().endswith(extensions):
            full_path = os.path.join(recording_path, f)
            files.append(full_path)
    
    if not files:
        return None

    newest_file = max(files, key=os.path.getmtime)

    try:
        stats = os.stat(newest_file)
        age = time.time() - stats.st_mtime
        if age > 120: 
            return None
    except Exception as e:
        print(f"Rename Script: Error checking file age. {e}")
        return None

    return newest_file

def show_custom_popup(filename):
    result = {"text": None}

    try:
        root = tk.Tk()
        root.title("Rename Recording") # Title changed
        
        # --- UI STYLING ---
        bg_color = "#2b2b2b"
        fg_color = "#ffffff" 
        entry_bg = "#3b3b3b"
        accent_color = "#D83C3E" # Changed to Red/Orange for "Rename" vibe
        
        root.configure(bg=bg_color)
        
        width, height = 400, 170
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        
        root.attributes("-topmost", True)
        root.lift()
        
        modern_font = ("Segoe UI", 11)
        bold_font = ("Segoe UI", 11, "bold")
        small_font = ("Segoe UI", 9)

        # Labels
        # Showing original name in small text so you know what you are renaming
        lbl_orig = tk.Label(root, text=f"Original: {filename}", 
                            bg=bg_color, fg="#aaaaaa", font=small_font, justify="left")
        lbl_orig.pack(pady=(15, 0), padx=20, anchor="w")

        lbl_main = tk.Label(root, text="Enter new filename:", 
                            bg=bg_color, fg=fg_color, font=bold_font, justify="left")
        lbl_main.pack(pady=(5, 5), padx=20, anchor="w")

        # Entry
        entry = tk.Entry(root, bg=entry_bg, fg=fg_color, insertbackground="white", 
                         font=modern_font, relief="flat")
        entry.pack(fill="x", padx=20, pady=5, ipady=3)
        entry.focus_force()

        def submit():
            raw_text = entry.get()
            clean_text = sanitize_filename(raw_text)
            if clean_text:
                result["text"] = clean_text
            root.destroy()
            
        def cancel(event=None):
            root.destroy()

        # Button
        btn = tk.Button(root, text="Rename File", command=submit, 
                        bg=accent_color, fg="white", activebackground="#a62e2f", 
                        font=bold_font, relief="flat", cursor="hand2")
        btn.pack(pady=10, ipadx=10)

        root.bind('<Return>', lambda event: submit())
        root.bind('<Escape>', cancel)
        root.protocol("WM_DELETE_WINDOW", cancel)

        root.mainloop()
    except Exception as e:
        print(f"Rename Script: UI Error - {e}")
        
    return result["text"]

def rename_process():
    time.sleep(rename_delay)

    old_file_path = find_newest_fresh_video()
    if not old_file_path:
        return

    current_name = os.path.basename(old_file_path)
    
    # Show Popup
    new_name_core = show_custom_popup(current_name)
    
    if not new_name_core:
        print("Rename Script: No name entered. Keeping original filename.")
        return

    directory = os.path.dirname(old_file_path)
    # Get extension from original file
    _, extension = os.path.splitext(current_name)
    
    # --- CONSTRUCT NEW FILENAME ---
    new_filename = f"{new_name_core}{extension}"
    new_file_path = os.path.join(directory, new_filename)

    # --- DUPLICATE CHECKER ---
    # If "MyGame.mp4" exists, change to "MyGame (1).mp4", then "MyGame (2).mp4"
    counter = 1
    while os.path.exists(new_file_path):
        new_filename = f"{new_name_core} ({counter}){extension}"
        new_file_path = os.path.join(directory, new_filename)
        counter += 1

    try:
        os.rename(old_file_path, new_file_path)
        print(f"Rename Script: Renamed to {new_filename}")
    except OSError as e:
        print(f"Rename Script: FAILED to rename. {e}")

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        t = threading.Thread(target=rename_process)
        t.start()

def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)