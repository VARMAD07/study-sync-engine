import shutil
import json
import time
from pathlib import Path
from scanner import DocumentScanner
from broker import EventBroker
from logger import CrashLogger  # <-- NEW: Connect the Diagnostic Shield

class StudySyncEngine:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir).expanduser()
        self.taxonomy = self.load_config()
        self.scanner = DocumentScanner()
        self.broker = EventBroker()
        self.logger = CrashLogger()  # <-- NEW: Initialize Logger

    def load_config(self):
        current_dir = Path(__file__).parent
        config_path = current_dir / "config.json"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.log_exception("Failed to safely read config.json", e)
            return {"Unsorted": [".pdf", ".txt", ".jpg"]}

    def categorize_file(self, item):
        try:
            ext = item.suffix.lower()
            if ext == ".pdf":
                deep_category = self.scanner.scan_pdf(item)
                if deep_category: return deep_category
            elif ext in [".png", ".jpg", ".jpeg"]:
                deep_category = self.scanner.scan_image(item)
                if deep_category: return deep_category
                    
            for category, extensions in self.taxonomy.items():
                if ext in extensions: return category
            return None
        except Exception as e:
            self.logger.log_exception(f"Error parsing metadata for file: {item.name}", e)
            return None

    def organize(self):
        move_log = []
        if not self.target_dir.exists():
            error_msg = "⚠️ ERROR: Target directory not found."
            self.broker.publish("file_moved", error_msg)
            return [error_msg]

        try:
            items_to_process = [item for item in self.target_dir.iterdir() if not item.is_dir()]
        except Exception as e:
            self.logger.log_exception("Failed to read directories iteration bounds", e)
            return ["❌ Critical storage lockout exception."]
        
        if not items_to_process:
            self.broker.publish("file_moved", "✨ Workspace is already pristine. No actions required.")
            return []

        for item in items_to_process:
            category = self.categorize_file(item)
            if category:
                destination_dir = self.target_dir / category
                destination_dir.mkdir(parents=True, exist_ok=True) 
                destination_path = destination_dir / item.name
                
                try:
                    shutil.move(str(item), str(destination_path))
                    log_line = f"✅ Sorted: {item.name} ➔ {category}/"
                    self.broker.publish("file_moved", log_line)
                    move_log.append(log_line)
                    time.sleep(0.05)
                except Exception as e:
                    # Capture exact operating system lockouts or access rights failures
                    self.logger.log_exception(f"OS file system access restriction on: {item.name}", e)
                    fail_line = f"❌ System Lockout: {item.name}"
                    self.broker.publish("file_moved", fail_line)
                    move_log.append(fail_line)
                    
        return move_log