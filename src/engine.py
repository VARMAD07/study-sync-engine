import shutil
import json
from pathlib import Path

class StudySyncEngine:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir).expanduser()
        self.taxonomy = self.load_config()

    def load_config(self):
        """Loads the sorting rules from our config.json file."""
        # Find exactly where this python file lives, then look for config.json next to it
        current_dir = Path(__file__).parent
        config_path = current_dir / "config.json"
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                print("[SYSTEM] Successfully loaded config.json")
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ [WARNING] config.json missing! Using fallback rules.")
            # Fallback just in case the file gets deleted
            return {"Unsorted": [".pdf", ".txt", ".jpg"]}

    def categorize_file(self, file_extension):
        """Checks the file extension against our loaded taxonomy."""
        ext = file_extension.lower()
        for category, extensions in self.taxonomy.items():
            if ext in extensions:
                return category
        return None

    def organize(self):
        print(f"[SCAN] Evaluating workspace: {self.target_dir}")
        
        if not self.target_dir.exists():
            print(f"[ERROR] Directory not found: {self.target_dir}")
            return

        for item in self.target_dir.iterdir():
            # Skip folders
            if item.is_dir():
                continue
                
            category = self.categorize_file(item.suffix)
            
            if category:
                destination_dir = self.target_dir / category
                destination_dir.mkdir(exist_ok=True)
                destination_path = destination_dir / item.name
                
                try:
                    shutil.move(str(item), str(destination_path))
                    print(f"[SUCCESS] Moved: {item.name} -> {category}/")
                except Exception as e:
                    print(f"[ERROR] Failed to move {item.name}: {str(e)}")

# (We don't need the bottom "if __name__ == '__main__'" testing block anymore 
# because our GUI handles running the engine now!)