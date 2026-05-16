import shutil
import json
from pathlib import Path
from scanner import DocumentScanner  # <-- NEW: Bring in the brain

class StudySyncEngine:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir).expanduser()
        self.taxonomy = self.load_config()
        self.scanner = DocumentScanner() # <-- NEW: Initialize the scanner

    def load_config(self):
        current_dir = Path(__file__).parent
        config_path = current_dir / "config.json"
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"Unsorted": [".pdf", ".txt", ".jpg"]}

    def categorize_file(self, item):
        """Upgraded categorization logic."""
        ext = item.suffix.lower()
        
        # --- THE COGNITIVE UPGRADE ---
        # If it's a PDF, don't just use the extension. Actually read it.
        if ext == ".pdf":
            deep_category = self.scanner.scan_pdf(item)
            if deep_category:
                return deep_category
                
        # For everything else (or if PDF reading fails), fallback to the standard config
        for category, extensions in self.taxonomy.items():
            if ext in extensions:
                return category
        return None

    def organize(self):
        move_log = []
        
        if not self.target_dir.exists():
            return ["⚠️ ERROR: Directory not found."]

        for item in self.target_dir.iterdir():
            if item.is_dir():
                continue
                
            # Pass the whole item object now, not just the extension
            category = self.categorize_file(item)
            
            if category:
                # This handles subfolders like "Academics/Physics" automatically
                destination_dir = self.target_dir / category
                destination_dir.mkdir(parents=True, exist_ok=True) 
                destination_path = destination_dir / item.name
                
                try:
                    shutil.move(str(item), str(destination_path))
                    move_log.append(f"✅ {item.name}  ➔  {category}/")
                except Exception as e:
                    move_log.append(f"❌ Failed: {item.name}")
                    
        return move_log