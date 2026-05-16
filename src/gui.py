import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import json
from pathlib import Path
from engine import StudySyncEngine
from focus import FocusMode
from stats import StatsManager
from broker import EventBroker
from watcher import FileWarden  # <-- NEW: Connecting the Warden background thread

class StudySyncUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Study Sync Engine - Enterprise Edition")
        self.window.geometry("450x680")  # Resized layout matrix
        self.window.configure(bg="#1E1E1E")
        
        self.selected_folder = tk.StringVar()
        self.selected_folder.set("No folder selected yet...")
        
        self.time_left = 0
        self.session_kills = 0  
        self.session_minutes = 0 
        self.is_locked_down = False
        self.warden_active = False
        self.warden_instance = None
        
        self.focuser = FocusMode()
        self.stats_manager = StatsManager()
        
        self.broker = EventBroker()
        self.broker.subscribe("file_moved", self._handle_live_stream_event)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", bg="#2D2D2D", fg="white", fieldbackground="#2D2D2D", font=("Helvetica", 9))
        self.style.configure("Treeview.Heading", bg="#4A4A4A", fg="white", font=("Helvetica", 9, "bold"))

        # --- ANALYTICS BAR ---
        stats_frame = tk.Frame(window, bg="#2D2D2D", pady=10)
        stats_frame.pack(fill="x")
        
        self.stat_label = tk.Label(stats_frame, text=self.get_stats_string(), fg="#E0A800", bg="#2D2D2D", font=("Consolas", 10, "bold"))
        self.stat_label.pack()

        # --- DYNAMIC CENTRAL DISPLAY ---
        self.display_frame = tk.Frame(window, bg="#1E1E1E")
        self.display_frame.pack(fill="x", pady=10)
        
        tk.Label(self.display_frame, text="Study Workspace Organizer", fg="white", bg="#1E1E1E", font=("Helvetica", 14, "bold")).pack()
        
        self.path_label = tk.Label(self.display_frame, textvariable=self.selected_folder, fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 10))
        self.path_label.pack(pady=5)

        # --- CENTRAL DIGITAL TIMER PANEL ---
        self.timer_label = tk.Label(window, text="00:00:00", fg="#E0A800", bg="#1E1E1E", font=("Consolas", 36, "bold"))

        # --- INTERACTIVE INTERFACE BUTTONS ---
        self.control_buttons_frame = tk.Frame(window, bg="#1E1E1E")
        self.control_buttons_frame.pack(fill="x")

        self.btn_select = tk.Button(self.control_buttons_frame, text="Select Folder", command=self.choose_folder, bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat")
        self.btn_select.pack(pady=5)
        
        self.btn_org = tk.Button(self.control_buttons_frame, text="Organize Now", command=self.run_engine, bg="#28A745", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        self.btn_org.pack(pady=5)

        # NEW: The Automation File Warden Toggle Switch
        self.btn_warden = tk.Button(self.control_buttons_frame, text="🟢 Activate Smart File Warden (Auto-Sort)", command=self.toggle_warden, bg="#1E1E1E", fg="#28A745", font=("Helvetica", 10, "bold"), relief="groove", bd=2)
        self.btn_warden.pack(pady=10)
        
        self.btn_focus = tk.Button(self.control_buttons_frame, text="🎯 Initiate Commitment Protocol", command=self.open_commitment_protocol, bg="#E0A800", fg="#1E1E1E", font=("Helvetica", 10, "bold"), relief="flat")
        self.btn_focus.pack(pady=5)
        
        self.btn_hitlist = tk.Button(self.control_buttons_frame, text="⚙️ Configure Target Hitlist", command=self.configure_hitlist, bg="#4A4A4A", fg="white", font=("Helvetica", 9), relief="flat")
        self.btn_hitlist.pack(pady=2)

        self.btn_rules = tk.Button(self.control_buttons_frame, text="📂 Manage Sorting Taxonomies", command=self.configure_taxonomies, bg="#3A3A3A", fg="#4DABF7", font=("Helvetica", 9, "bold"), relief="flat")
        self.btn_rules.pack(pady=5)

        # --- LIVE SYSTEM AUDIT LOG ---
        self.log_box = tk.Listbox(window, bg="#2D2D2D", fg="#4DABF7", font=("Consolas", 9), relief="flat", highlightthickness=0)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Bind closing handle cleanup method to avoid ghost background tasks surviving
        self.window.protocol("WM_DELETE_WINDOW", self.on_close_cleanup)

    def get_stats_string(self):
        s = self.stats_manager.stats
        return f"🏆 LIFETIME FOCUS: {s['total_focus_minutes']} MINS | 🛑 DISTRACTIONS DEFEATED: {s['distractions_killed']}"

    def update_stats_display(self):
        self.stat_label.config(text=self.get_stats_string())

    def choose_folder(self):
        if self.is_locked_down or self.warden_active: return
        folder_path = filedialog.askdirectory(title="Pick a messy folder")
        if folder_path:
            self.selected_folder.set(folder_path)

    def run_engine(self):
        if self.is_locked_down: return
        target = self.selected_folder.get()
        if target == "No folder selected yet...":
            self.path_label.config(text="⚠️ Please select a folder first!", fg="#FF6B6B")
            return
            
        self.log_box.delete(0, tk.END)
        self.log_box.insert(tk.END, "[SYSTEM] Spawning background worker thread...")
        self.path_label.config(text="ASYNC WORKER ACTIVE...", fg="#007ACC")

        def worker_loop():
            sorter = StudySyncEngine(target_dir=target)
            results = sorter.organize()
            self.window.after(0, self._finalize_engine_ui, results)

        threading.Thread(target=worker_loop, daemon=True).start()

    def _finalize_engine_ui(self, results):
        self.log_box.delete(0, tk.END)
        for line in (results if results else ["✨ No files needed moving. Workspace is clean."]):
            self.log_box.insert(tk.END, line)
        if not self.is_locked_down and not self.warden_active:
            self.path_label.config(text="✅ Workspace Cleaned!", fg="#4DABF7")

    def _handle_live_stream_event(self, event_message):
        self.window.after(0, lambda: self.log_box.insert(tk.END, event_message))
        self.window.after(0, lambda: self.log_box.yview(tk.END))

    # --- NEW: WARDEN AUTOMATION CONTROLLER ---
    def toggle_warden(self):
        if self.is_locked_down: return
        target = self.selected_folder.get()
        if target == "No folder selected yet...":
            messagebox.showerror("Error", "Please explicitly select a folder directory to monitor first.")
            return

        if not self.warden_active:
            # Activate the Watchdog loop
            self.warden_instance = FileWarden(target)
            self.warden_instance.start()
            self.warden_active = True
            
            self.btn_warden.config(text="🔴 Deactivate Warden (Sorting Active)", fg="#FF6B6B", bg="#2D2D2D")
            self.btn_select.config(state="disabled")
            self.btn_org.config(state="disabled")
            self.path_label.config(text="🔒 AUTOMATION MONITORING ENGAGED", fg="#28A745")
            self.log_box.insert(tk.END, "🚀 [AUTOMATION] Warden deployed. Drop files into folder to test.")
        else:
            # Terminate Watchdog thread safely
            if self.warden_instance:
                self.warden_instance.stop()
            self.warden_active = False
            
            self.btn_warden.config(text="🟢 Activate Smart File Warden (Auto-Sort)", fg="#28A745", bg="#1E1E1E")
            self.btn_select.config(state="normal")
            self.btn_org.config(state="normal")
            self.path_label.config(text="✅ Back to manual tracking.", fg="#4DABF7")

    def on_close_cleanup(self):
        """Safely unhooks Windows directory sensors on close to prevent process leakages."""
        if self.warden_active and self.warden_instance:
            self.warden_instance.stop()
        self.window.destroy()

    # --- TAXONOMY CONTROLS ---
    def configure_taxonomies(self):
        if self.is_locked_down: return
        popup = tk.Toplevel(self.window)
        popup.title("Taxonomy Manager")
        popup.geometry("450x500")
        popup.configure(bg="#1E1E1E")
        popup.attributes("-topmost", True)
        
        tk.Label(popup, text="Active Classification Maps", fg="white", bg="#1E1E1E", font=("Helvetica", 12, "bold")).pack(pady=10)
        config_path = Path(__file__).parent / "config.json"
        
        grid_frame = tk.Frame(popup, bg="#1E1E1E")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        columns = ("folder", "extensions")
        tree = ttk.Treeview(grid_frame, columns=columns, show="headings", height=8)
        tree.heading("folder", text="Target Category Folder")
        tree.heading("extensions", text="Monitored Extensions")
        tree.column("folder", width=180, anchor="w")
        tree.column("extensions", width=200, anchor="w")
        tree.pack(fill="both", expand=True)
        
        def refresh_grid_display():
            for item in tree.get_children(): tree.delete(item)
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for folder, exts in data.items():
                    tree.insert("", tk.END, values=(folder, ", ".join(exts)))
            except Exception: pass
                
        refresh_grid_display()
        
        input_frame = tk.Frame(popup, bg="#1E1E1E")
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text="Folder Name:", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        folder_entry = tk.Entry(input_frame, width=25, bg="#2D2D2D", fg="white", font=("Helvetica", 10), relief="flat")
        folder_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(input_frame, text="Extensions:", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", padx=5)
        ext_entry = tk.Entry(input_frame, width=25, bg="#2D2D2D", fg="white", font=("Helvetica", 10), relief="flat")
        ext_entry.insert(0, ".mp3, .wav")
        ext_entry.grid(row=1, column=1, pady=5, padx=5)

        def inject_new_rule():
            folder = folder_entry.get().strip()
            ext_strings = ext_entry.get().strip()
            if not folder or not ext_strings: return
            cleaned_extensions = [e.strip().lower() if e.strip().startswith(".") else f".{e.strip().lower()}" for e in ext_strings.split(",")]
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    current_taxonomy = json.load(f)
                current_taxonomy[folder] = list(set(current_taxonomy.get(folder, []) + cleaned_extensions))
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(current_taxonomy, f, indent=4)
                refresh_grid_display()
                folder_entry.delete(0, tk.END)
                ext_entry.delete(0, tk.END)
            except Exception: pass

        tk.Button(popup, text="➕ Inject Sorter Rule", command=inject_new_rule, bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat", pady=4).pack(pady=10)

    # --- HITLIST CONTROLS ---
    def configure_hitlist(self):
        if self.is_locked_down: return
        popup = tk.Toplevel(self.window)
        popup.title("Target Hitlist")
        popup.geometry("350x450")
        popup.configure(bg="#1E1E1E")
        popup.attributes("-topmost", True)
        
        tk.Label(popup, text="Active Distraction Targets", fg="white", bg="#1E1E1E", font=("Helvetica", 12, "bold")).pack(pady=10)
        self.focuser.load_hitlist()
        self.check_vars = {}
        
        list_frame = tk.Frame(popup, bg="#1E1E1E")
        list_frame.pack(fill="both", expand=True, padx=20)

        for app_name, data in self.focuser.distractions.items():
            var = tk.BooleanVar(value=data["active"])
            self.check_vars[app_name] = var
            cb = tk.Checkbutton(list_frame, text=app_name, variable=var, bg="#1E1E1E", fg="#4DABF7", selectcolor="#2D2D2D", activebackground="#1E1E1E", activeforeground="white", font=("Helvetica", 10, "bold"))
            cb.pack(anchor="w", pady=2)
            
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
            for app, var in self.check_vars.items(): self.focuser.distractions[app]["active"] = var.get()
            new_name, new_exe = name_entry.get().strip(), exe_entry.get().strip()
            if new_name and new_exe and new_name != "Name" and new_exe != "app.exe":
                if not new_exe.endswith(".exe"): new_exe += ".exe"
                self.focuser.distractions[new_name] = {"exe": new_exe, "active": True}
            self.focuser.save_hitlist()
            popup.destroy()
            
        tk.Button(popup, text="Save Settings", command=save_and_close, bg="#007ACC", fg="white", font=("Helvetica", 10, "bold"), relief="flat").pack(pady=15)

    # --- COMMITMENT PROTOCOL ---
    def open_commitment_protocol(self):
        if self.is_locked_down: return
        popup = tk.Toplevel(self.window)
        popup.title("The Oath")
        popup.geometry("320x300")
        popup.configure(bg="#1E1E1E")
        popup.attributes("-topmost", True) 

        tk.Label(popup, text="Set Lockdown Duration", fg="white", bg="#1E1E1E", font=("Helvetica", 12, "bold")).pack(pady=10)
        t_frame = tk.Frame(popup, bg="#1E1E1E")
        t_frame.pack(pady=5)
        
        tk.Label(t_frame, text="HRS", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 8)).grid(row=0, column=0)
        tk.Label(t_frame, text="MIN", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 8)).grid(row=0, column=1)
        tk.Label(t_frame, text="SEC", fg="#A0A0A0", bg="#1E1E1E", font=("Helvetica", 8)).grid(row=0, column=2)

        h_entry = tk.Entry(t_frame, width=4, bg="#2D2D2D", fg="white", justify="center", font=("Helvetica", 12))
        h_entry.insert(0, "00")
        h_entry.grid(row=1, column=0, padx=5)
        m_entry = tk.Entry(t_frame, width=4, bg="#2D2D2D", fg="white", justify="center", font=("Helvetica", 12))
        m_entry.insert(0, "01")
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
                    h, m, s = int(h_entry.get()), int(m_entry.get()), int(s_entry.get())
                    total_seconds = (h * 3600) + (m * 60) + s
                    if total_seconds <= 0: raise ValueError
                    popup.destroy()
                    self.start_lockdown(total_seconds, max(1, total_seconds // 60))
                except ValueError: messagebox.showerror("Error", "Please enter valid time values.")
            else: messagebox.showerror("Failure", "You must type the oath exactly to proceed.")

        tk.Button(popup, text="Lock In", command=verify_and_lock, bg="#E0A800", fg="#1E1E1E", font=("Helvetica", 10, "bold"), relief="flat").pack(pady=20)

    def start_lockdown(self, total_seconds, total_minutes):
        self.is_locked_down = True
        self.time_left = total_seconds
        self.session_minutes = total_minutes
        self.session_kills = 0 
        self.control_buttons_frame.pack_forget()
        self.timer_label.pack(pady=15)
        self.log_box.delete(0, tk.END)
        self.log_box.insert(tk.END, "--- 🔒 PROTOCOL ENGAGED ---")
        self.tick_timer()

    def tick_timer(self):
        if self.time_left > 0:
            h, rem = divmod(self.time_left, 3600)
            m, s = divmod(rem, 60)
            self.timer_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            self.path_label.config(text="🔒 ENVIRONMENT LOCKED DOWN", fg="#E0A800")
            if self.time_left % 5 == 0:
                kills = self.focuser.engage(silent=True)
                for k in kills:
                    self.log_box.insert(tk.END, k)
                    self.session_kills += 1 
            self.time_left -= 1
            self.window.after(1000, self.tick_timer)
        else:
            self.is_locked_down = False
            self.timer_label.pack_forget()
            self.control_buttons_frame.pack(fill="x", before=self.log_box)
            self.path_label.config(text="✅ Session Complete.", fg="#28A745")
            self.stats_manager.log_session(self.session_minutes, self.session_kills)
            self.update_stats_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudySyncUI(root)
    root.mainloop()