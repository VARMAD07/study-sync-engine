import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from engine import StudySyncEngine
from focus import FocusMode

class StudySyncUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Study Sync Engine")
        self.window.geometry("450x500")
        self.window.configure(bg="#1E1E1E")
        
        self.selected_folder = tk.StringVar()
        self.selected_folder.set("No folder selected yet...")
        self.time_left = 0
        self.focuser = FocusMode()

        # --- MAIN MENU UI ---
        tk.Label(window, text="Study Workspace Organizer", fg="white", bg="#1E1E1E", font=("Helvetica", 14, "bold")).pack(pady=10)
        self.path_label = tk.Label(window, textvariable=self.selected_folder, fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 10))
        self.path_label.pack(pady=5)

        tk.Button(window, text="Select Folder", command=self.choose_folder, bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat").pack(pady=5)
        tk.Button(window, text="Organize Now", command=self.run_engine, bg="#28A745", fg="white", font=("Helvetica", 12, "bold"), relief="flat").pack(pady=5)
        
        tk.Button(window, text="🎯 Initiate Commitment Protocol", command=self.open_commitment_protocol, bg="#E0A800", fg="#1E1E1E", font=("Helvetica", 10, "bold"), relief="flat").pack(pady=10)
        tk.Button(window, text="⚙️ Configure Target Hitlist", command=self.configure_hitlist, bg="#4A4A4A", fg="white", font=("Helvetica", 9), relief="flat").pack(pady=5)

        self.log_box = tk.Listbox(window, bg="#2D2D2D", fg="#4DABF7", font=("Consolas", 9), relief="flat", highlightthickness=0)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # --- UI ACTIONS ---
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
        for line in (results if results else ["✨ No files needed moving."]):
            self.log_box.insert(tk.END, line)
        self.path_label.config(text="✅ Workspace Cleaned!", fg="#4DABF7")

    # --- THE HITLIST DASHBOARD ---
    def configure_hitlist(self):
        popup = tk.Toplevel(self.window)
        popup.title("Target Hitlist")
        popup.geometry("350x450")
        popup.configure(bg="#1E1E1E")
        popup.attributes("-topmost", True)
        
        tk.Label(popup, text="Active Distraction Targets", fg="white", bg="#1E1E1E", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        self.focuser.load_hitlist()
        self.check_vars = {}
        
        # Frame for the checkboxes
        list_frame = tk.Frame(popup, bg="#1E1E1E")
        list_frame.pack(fill="both", expand=True, padx=20)

        for app_name, data in self.focuser.distractions.items():
            var = tk.BooleanVar(value=data["active"])
            self.check_vars[app_name] = var
            cb = tk.Checkbutton(list_frame, text=app_name, variable=var, bg="#1E1E1E", fg="#4DABF7", selectcolor="#2D2D2D", activebackground="#1E1E1E", activeforeground="white", font=("Helvetica", 10, "bold"))
            cb.pack(anchor="w", pady=2)
            
        # Add Custom App Section
        tk.Label(popup, text="Add Custom Target (e.g. Valorant / valorant.exe)", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 8)).pack(pady=(10, 0))
        add_frame = tk.Frame(popup, bg="#1E1E1E")
        add_frame.pack(pady=5)
        
        name_entry = tk.Entry(add_frame, width=12, bg="#2D2D2D", fg="white", font=("Helvetica", 9))
        name_entry.insert(0, "Name")
        name_entry.grid(row=0, column=0, padx=2)
        
        exe_entry = tk.Entry(add_frame, width=15, bg="#2D2D2D", fg="white", font=("Helvetica", 9))
        exe_entry.insert(0, "app.exe")
        exe_entry.grid(row=0, column=1, padx=2)

        def save_and_close():
            # Save checkbox states
            for app, var in self.check_vars.items():
                self.focuser.distractions[app]["active"] = var.get()
            
            # Save new app if entered
            new_name = name_entry.get().strip()
            new_exe = exe_entry.get().strip()
            if new_name and new_exe and new_name != "Name" and new_exe != "app.exe":
                if not new_exe.endswith(".exe"): new_exe += ".exe"
                self.focuser.distractions[new_name] = {"exe": new_exe, "active": True}
                
            self.focuser.save_hitlist()
            popup.destroy()
            
        tk.Button(popup, text="Save Settings", command=save_and_close, bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat").pack(pady=15)

    # --- THE COMMITMENT PROTOCOL (UPGRADED TIMER) ---
    def open_commitment_protocol(self):
        popup = tk.Toplevel(self.window)
        popup.title("The Oath")
        popup.geometry("320x300")
        popup.configure(bg="#1E1E1E")
        popup.attributes("-topmost", True) 

        tk.Label(popup, text="Set Lockdown Duration", fg="white", bg="#1E1E1E", font=("Helvetica", 12, "bold")).pack(pady=10)

        # Time Entry Frame
        t_frame = tk.Frame(popup, bg="#1E1E1E")
        t_frame.pack(pady=5)
        
        tk.Label(t_frame, text="HRS", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 8)).grid(row=0, column=0)
        tk.Label(t_frame, text="MIN", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 8)).grid(row=0, column=1)
        tk.Label(t_frame, text="SEC", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 8)).grid(row=0, column=2)

        h_entry = tk.Entry(t_frame, width=4, bg="#2D2D2D", fg="white", justify="center", font=("Helvetica", 12))
        h_entry.insert(0, "00")
        h_entry.grid(row=1, column=0, padx=5)

        m_entry = tk.Entry(t_frame, width=4, bg="#2D2D2D", fg="white", justify="center", font=("Helvetica", 12))
        m_entry.insert(0, "60")
        m_entry.grid(row=1, column=1, padx=5)

        s_entry = tk.Entry(t_frame, width=4, bg="#2D2D2D", fg="white", justify="center", font=("Helvetica", 12))
        s_entry.insert(0, "00")
        s_entry.grid(row=1, column=2, padx=5)

        tk.Label(popup, text="Type: 'I commit to focus'", fg="#FF6B6B", bg="#1E1E1E", font=("Helvetica", 10, "bold")).pack(pady=15)
        oath_entry = tk.Entry(popup, bg="#2D2D2D", fg="white", justify="center", width=25, font=("Helvetica", 12))
        oath_entry.pack()

        def verify_and_lock():
            if oath_entry.get().strip().lower() == "i commit to focus":
                try:
                    h = int(h_entry.get())
                    m = int(m_entry.get())
                    s = int(s_entry.get())
                    total_seconds = (h * 3600) + (m * 60) + s
                    
                    if total_seconds <= 0:
                        raise ValueError
                        
                    popup.destroy()
                    self.start_lockdown(total_seconds)
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid time values.")
            else:
                messagebox.showerror("Failure", "You must type the oath exactly to proceed.")

        tk.Button(popup, text="Lock In", command=verify_and_lock, bg="#E0A800", fg="#1E1E1E", font=("Helvetica", 10, "bold"), relief="flat").pack(pady=20)

    # --- THE TIMER & BACKGROUND HUNTER ---
    def start_lockdown(self, total_seconds):
        self.time_left = total_seconds
        self.log_box.delete(0, tk.END)
        self.log_box.insert(tk.END, "--- 🔒 PROTOCOL ENGAGED ---")
        self.log_box.insert(tk.END, "Guard dog is active. Do not open distractions.")
        self.tick_timer()

    def tick_timer(self):
        if self.time_left > 0:
            h, rem = divmod(self.time_left, 3600)
            m, s = divmod(rem, 60)
            
            # Format nicely as HH:MM:SS
            self.path_label.config(text=f"🔒 LOCKDOWN ACTIVE: {h:02d}:{m:02d}:{s:02d}", fg="#E0A800")
            
            if self.time_left % 5 == 0:
                kills = self.focuser.engage(silent=True)
                for k in kills:
                    self.log_box.insert(tk.END, k)
                    self.log_box.yview(tk.END)
                    
            self.time_left -= 1
            self.window.after(1000, self.tick_timer)
        else:
            self.path_label.config(text="✅ Session Complete. Excellent work.", fg="#28A745")
            self.log_box.insert(tk.END, "--- 🔓 PROTOCOL LIFTED ---")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudySyncUI(root)
    root.mainloop()