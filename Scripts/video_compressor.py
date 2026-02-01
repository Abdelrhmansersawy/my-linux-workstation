import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import time

# --- Configuration ---
CRF = "23"
PRESET = "medium"

# --- Global State ---
queue_data = {} 
is_processing = False

def format_size(size):
    # Helper to make file sizes human readable
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def add_files():
    files = filedialog.askopenfilenames(
        title="Select Videos",
        filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv")]
    )
    if not files:
        return

    for f in files:
        # Avoid duplicates based on path
        existing_paths = [data['path'] for data in queue_data.values()]
        if f in existing_paths:
            continue

        file_name = os.path.basename(f)
        try:
            size_bytes = os.path.getsize(f)
            size_str = format_size(size_bytes)
        except OSError:
            size_str = "Unknown"

        # Insert into Treeview
        item_id = tree.insert(
            "", 
            "end", 
            values=(file_name, size_str, "Queued", "0%")
        )
        
        # Store data for processing later
        queue_data[item_id] = {
            "path": f,
            "status": "Queued"
        }

def remove_selected():
    selected_item = tree.selection()
    if selected_item:
        for item in selected_item:
            tree.delete(item)
            if item in queue_data:
                del queue_data[item]

def clear_all():
    for item in tree.get_children():
        tree.delete(item)
    queue_data.clear()

def get_duration(video):
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video
        ]
        # Prevent console window popup on Windows
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        result = subprocess.run(cmd, capture_output=True, text=True, startupinfo=startupinfo)
        return float(result.stdout.strip())
    except Exception:
        return 0

def compress_single_video(item_id):
    data = queue_data[item_id]
    input_file = data["path"]
    output_file = os.path.splitext(input_file)[0] + "_compressed.mp4"
    
    # Update Status
    tree.set(item_id, "status", "Analyzing...")
    duration = get_duration(input_file)
    
    if duration == 0:
        tree.set(item_id, "status", "Error (Probe)")
        return

    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-c:v", "libx264",
        "-preset", PRESET,
        "-crf", CRF,
        "-c:a", "aac",
        "-b:a", "128k",
        "-progress", "pipe:1",
        "-nostats",
        output_file
    ]

    tree.set(item_id, "status", "Compressing...")

    # Hide console window on Windows
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        startupinfo=startupinfo
    )

    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        
        if line:
            if "out_time_ms" in line:
                try:
                    ms = int(line.split("=")[1].strip())
                    seconds = ms / 1_000_000
                    percent = min((seconds / duration) * 100, 100)
                    
                    # Update Treeview UI
                    tree.set(item_id, "progress", f"{percent:.1f}%")
                except (ValueError, IndexError):
                    pass

    if process.returncode == 0:
        tree.set(item_id, "status", "Completed")
        tree.set(item_id, "progress", "100%")
    else:
        tree.set(item_id, "status", "Error")

def start_processing():
    global is_processing
    if is_processing:
        return
    
    if not queue_data:
        messagebox.showwarning("Empty Queue", "Please add videos first.")
        return

    def worker():
        global is_processing
        is_processing = True
        btn_start.config(state="disabled")
        
        # Iterate through all items in the tree
        for item_id in tree.get_children():
            # Only process queued items
            current_status = tree.item(item_id, "values")[2]
            if current_status == "Queued":
                compress_single_video(item_id)
        
        is_processing = False
        btn_start.config(state="normal")
        messagebox.showinfo("Done", "Queue processing finished!")

    threading.Thread(target=worker, daemon=True).start()

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Internet Manager Video Compressor")
root.geometry("800x500")

# Apply a modern style
style = ttk.Style()
style.theme_use("clam") 

# Customizing Treeview colors
style.configure("Treeview", 
    background="white",
    foreground="black",
    rowheight=25,
    fieldbackground="white"
)
style.map('Treeview', background=[('selected', '#3498db')])

# --- Header / Toolbar ---
toolbar_frame = tk.Frame(root, bg="#f0f0f0", bd=1, relief="raised")
toolbar_frame.pack(side="top", fill="x")

# Toolbar Buttons
def create_tool_btn(parent, text, icon, cmd, color="#333"):
    frame = tk.Frame(parent, bg="#f0f0f0")
    frame.pack(side="left", padx=5, pady=5)
    
    btn = tk.Button(
        frame, 
        text=f"{icon}\n{text}", 
        font=("Segoe UI", 9), 
        bg="#e1e1e1", 
        fg=color,
        relief="flat",
        width=10,
        height=2,
        command=cmd
    )
    btn.pack()
    return btn

create_tool_btn(toolbar_frame, "Add Files", "➕", add_files, "#006400")
btn_start = create_tool_btn(toolbar_frame, "Start Queue", "▶", start_processing, "#00008B")
create_tool_btn(toolbar_frame, "Remove", "❌", remove_selected, "#8B0000")
create_tool_btn(toolbar_frame, "Clear All", "🗑", clear_all)

# --- Main Grid Area ---
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("file", "size", "status", "progress")
tree = ttk.Treeview(main_frame, columns=columns, show="headings", selectmode="extended")

# Define Headings
tree.heading("file", text="File Name", anchor="w")
tree.heading("size", text="Size", anchor="center")
tree.heading("status", text="Status", anchor="center")
tree.heading("progress", text="Progress", anchor="center")

# Define Columns Width
tree.column("file", width=350, anchor="w")
tree.column("size", width=100, anchor="center")
tree.column("status", width=120, anchor="center")
tree.column("progress", width=100, anchor="center")

# Scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Footer ---
status_bar = tk.Label(
    root, 
    text="Ready. Add files to begin.", 
    bd=1, 
    relief="sunken", 
    anchor="w",
    font=("Segoe UI", 8)
)
status_bar.pack(side="bottom", fill="x")

root.mainloop()