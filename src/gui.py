import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from engine import StudySyncEngine
from focus import FocusMode  # <-- NEW: Bringing in the weapon

class StudySyncUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Study Sync Engine")
        self.window.geometry("450x450") # Slightly taller for the new button
        self.window.configure(bg="#1E1E1E")
        
        self.selected_folder = tk.StringVar()
        self.selected_folder.set("No folder selected yet...")

        # --- UI ELEMENTS ---
        title_label = tk.Label(window, text="Study Workspace Organizer", fg="white", bg="#1E1E1E", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=10)

        self.path_label = tk.Label(window, textvariable=self.selected_folder, fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 10))
        self.path_label.pack(pady=5)

        select_btn = tk.Button(window, text="Select Folder", command=self.choose_folder, bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat")
        select_btn.pack(pady=5)

        run_btn = tk.Button(window, text="Organize Now", command=self.run_engine, bg="#28A745", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        run_btn.pack(pady=5)

        # NEW: The Focus Button
        focus_btn = tk.Button(window, text="🎯 Engage Focus Mode", command=self.run_focus, bg="#E0A800", fg="#1E1E1E", font=("Helvetica", 10, "bold"), relief="flat")
        focus_btn.pack(pady=10)

        self.log_box = tk.Listbox(window, bg="#2D2D2D", fg="#4DABF7", font=("Consolas", 9), relief="flat", highlightthickness=0)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def choose_folder(self):
        folder_path = filedialog.askdirectory(title="Pick a messy folder")
        if folder_path:
            self.selected_folder.set(folder_path)

    def run_engine(self):
        target = self.selected_folder.get()
        if target == "No folder selected yet...":
            self.path_label.config(text="⚠️ Please select a folder first!", fg="#FF6B6B")
            return
            
        sorter = StudySyncEngine(target_dir=target)
        results = sorter.organize()
        
        self.log_box.delete(0, tk.END)
        if not results:
            self.log_box.insert(tk.END, "✨ No files needed moving. Workspace is clean.")
        else:
            for line in results:
                self.log_box.insert(tk.END, line)
                
        self.path_label.config(text="✅ Workspace Cleaned!", fg="#4DABF7")

    # NEW: The Focus logic
    def run_focus(self):
        focuser = FocusMode()
        results = focuser.engage()
        
        self.log_box.delete(0, tk.END)
        self.log_box.insert(tk.END, "--- 🎯 FOCUS MODE ENGAGED ---")
        for line in results:
            self.log_box.insert(tk.END, line)
            
        self.path_label.config(text="Distractions Neutralized.", fg="#E0A800")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudySyncUI(root)
    root.mainloop()