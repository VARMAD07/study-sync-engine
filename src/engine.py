import shutil
import json
from pathlib import Path

class StudySyncEngine:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir).expanduser()
        self.taxonomy = self.load_config()

    def load_config(self):
        """Loads the sorting rules from our config.json file."""
        current_dir = Path(__file__).parent
        config_path = current_dir / "config.json"
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                print("[SYSTEM] Successfully loaded config.json")
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ [WARNING] config.json missing! Using fallback rules.")
            return {"Unsorted": [".pdf", ".txt", ".jpg"]}

    def categorize_file(self, file_extension):
        """Checks the file extension against our loaded taxonomy."""
        ext = file_extension.lower()
        for category, extensions in self.taxonomy.items():
            if ext in extensions:
                return category
        return None

    def organize(self):
        # This will store our "receipt"
        move_log = []
        
        if not self.target_dir.exists():
            return ["⚠️ ERROR: Directory not found."]

        for item in self.target_dir.iterdir():
            if item.is_dir():
                continue
                
            category = self.categorize_file(item.suffix)
            
            if category:
                destination_dir = self.target_dir / category
                destination_dir.mkdir(exist_ok=True)
                destination_path = destination_dir / item.name
                
                try:
                    shutil.move(str(item), str(destination_path))
                    # Add successful move to our log instead of just printing
                    move_log.append(f"✅ {item.name}  ➔  {category}/")
                except Exception as e:
                    move_log.append(f"❌ Failed: {item.name}")
                    
        return move_log