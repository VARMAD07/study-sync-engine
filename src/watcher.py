import time
from pathlib import Path
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from engine import StudySyncEngine

class WardenHandler(FileSystemEventHandler):
    def __init__(self, engine_instance):
        self.engine = engine_instance

    def on_created(self, event):
        # Ignore directories completely, we only target raw files
        if event.is_directory:
            return
            
        print(f"[WARDEN WATCH] New system file detected: {Path(event.src_path).name}")
        # Give the file a brief 200ms buffer to finish downloading completely
        time.sleep(0.2)
        
        # Trigger the engine sorting sequence automatically
        self.engine.organize()

class FileWarden:
    def __init__(self, watch_dir_path):
        self.watch_dir = Path(watch_dir_path).expanduser()
        self.engine = StudySyncEngine(target_dir=self.watch_dir)
        self.observer = Observer()
        self.running = False

    def start(self):
        """Launches the folder sensor channel on a separate background execution stream."""
        if not self.watch_dir.exists():
            print(f"[WARDEN ERROR] Monitored target path does not exist: {self.watch_dir}")
            return
            
        event_handler = WardenHandler(self.engine)
        self.observer.schedule(event_handler, path=str(self.watch_dir), recursive=False)
        self.observer.start()
        self.running = True
        print(f"🔒 [WARDEN SUCCESS] Continuous Watchdog deployed over: {self.watch_dir}")

    def stop(self):
        """Safely tears down the OS hook thread on close."""
        if self.running:
            self.observer.stop()
            self.observer.join()
            self.running = False
            print("🔓 [WARDEN OFF] Monitoring loop cleanly deactivated.")