import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from engine import StudySyncEngine

class StudySyncUI:
    def __init__(self, window):
        self.window = window
        # Let's make the window look modern, not like Windows 95
        self.window.title("Study Sync Engine")
        self.window.geometry("400x250")
        self.window.configure(bg="#1E1E1E") # Dark mode aesthetics
        
        # We need a variable to remember which folder the user picked
        self.selected_folder = tk.StringVar()
        self.selected_folder.set("No folder selected yet...")

        # --- UI ELEMENTS ---
        
        # 1. The Title Label
        title_label = tk.Label(window, text="Study Workspace Organizer", 
                               fg="white", bg="#1E1E1E", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=20) # pady adds some breathing room above and below

        # 2. The Text showing the chosen folder
        self.path_label = tk.Label(window, textvariable=self.selected_folder, 
                                   fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 10))
        self.path_label.pack(pady=5)

        # 3. The Button to choose a folder
        select_btn = tk.Button(window, text="Select Folder to Clean", command=self.choose_folder,
                               bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat")
        select_btn.pack(pady=10)

        # 4. The Big Action Button to run the engine
        run_btn = tk.Button(window, text="Organize Now", command=self.run_engine,
                            bg="#28A745", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        run_btn.pack(pady=15)

    def choose_folder(self):
        """Pops open a window to let you click and pick a folder."""
        folder_path = filedialog.askdirectory(title="Pick a messy folder")
        if folder_path:
            self.selected_folder.set(folder_path)

    def run_engine(self):
        """Grabs the folder you picked and hands it over to our engine to sort."""
        target = self.selected_folder.get()
        
        # Quick check so we don't try to sort nothing
        if target == "No folder selected yet...":
            self.path_label.config(text="⚠️ Please select a folder first!", fg="#FF6B6B")
            return
            
        # Fire up the engine we built earlier
        sorter = StudySyncEngine(target_dir=target)
        sorter.organize()
        
        # Let the user know we finished the job
        self.path_label.config(text="✅ Workspace Cleaned!", fg="#4DABF7")

# --- STARTUP LOGIC ---
if __name__ == "__main__":
    # Create the actual window
    root = tk.Tk()
    
    # Attach our UI design to it
    app = StudySyncUI(root)
    
    # Keep the window open and running
    root.mainloop()