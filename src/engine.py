import shutil
import json
import time
from pathlib import Path
from scanner import DocumentScanner
from broker import EventBroker
from logger import CrashLogger

class StudySyncEngine:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir).expanduser()
        self.config_path = Path(__file__).parent / "config.json"
        self.taxonomy = self.load_config()
        self.scanner = DocumentScanner()
        self.broker = EventBroker()
        self.logger = CrashLogger()

    def load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("taxonomy", {})
        except Exception as e:
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
            self.logger.log_exception(f"Metadata parsing failure: {item.name}", e)
            return None

    def resolve_safe_path(self, dest_dir, file_name):
        """--- THE COLLISION CURE --- Increments file index names if a duplicate exists."""
        base_path = Path(dest_dir) / file_name
        if not base_path.exists():
            return base_path
            
        stem = base_path.stem
        suffix = base_path.suffix
        counter = 1
        
        # Loop sequentially until an open slot (e.g., file_1.pdf, file_2.pdf) is located
        while (Path(dest_dir) / f"{stem}_{counter}{suffix}").exists():
            counter += 1
            
        return Path(dest_dir) / f"{stem}_{counter}{suffix}"

    def organize(self):
        move_log = []
        if not self.target_dir.exists():
            error_msg = "⚠️ ERROR: Directory path missing."
            self.broker.publish("file_moved", error_msg)
            return [error_msg]

        try:
            items_to_process = [item for item in self.target_dir.iterdir() if not item.is_dir()]
        except Exception as e:
            self.logger.log_exception("Directory processing block", e)
            return ["❌ Storage lockout error."]
        
        if not items_to_process:
            self.broker.publish("file_moved", "✨ Workspace is immaculate.")
            return []

        for item in items_to_process:
            category = self.categorize_file(item)
            if category:
                destination_dir = self.target_dir / category
                destination_dir.mkdir(parents=True, exist_ok=True) 
                
                # Dynamic safety path resolution pass
                final_destination = self.resolve_safe_path(destination_dir, item.name)
                
                try:
                    shutil.move(str(item), str(final_destination))
                    log_line = f"✅ Sorted: {item.name} ➔ {category}/{final_destination.name}"
                    self.broker.publish("file_moved", log_line)
                    move_log.append(log_line)
                    time.sleep(0.05)
                except Exception as e:
                    self.logger.log_exception(f"Access lockout on file: {item.name}", e)
                    fail_line = f"❌ System Lockout: {item.name}"
                    self.broker.publish("file_moved", fail_line)
                    move_log.append(fail_line)
                    
        return move_log