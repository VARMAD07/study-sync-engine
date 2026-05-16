import shutil
from pathlib import Path

class StudySyncEngine:
    def __init__(self, target_dir):
        # expanduser() safely figures out exactly where your computer's main user folder is
        self.target_dir = Path(target_dir).expanduser()
        
        # Our smart academic sorting rules
        self.TAXONOMY = {
            'Literature': ['.pdf', '.epub'],
            'Notes & Context': ['.docx', '.txt', '.md'],
            'Media & Assets': ['.png', '.jpg'],
            'Source Code': ['.py', '.ipynb', '.html']
        }

    def categorize_file(self, file_extension):
        """Checks the file extension against our taxonomy map."""
        ext = file_extension.lower()
        for category, extensions in self.TAXONOMY.items():
            if ext in extensions:
                return category
        return None

    def organize(self):
        print(f"[SCAN] Evaluating workspace: {self.target_dir}")
        
        if not self.target_dir.exists():
            print(f"[ERROR] Directory not found: {self.target_dir}")
            return

        for item in self.target_dir.iterdir():
            # Skip existing folders
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

if __name__ == "__main__":
    # We are pointing this safely at your Sandbox folder to protect your real files for now
    safe_target = Path.home() / "Desktop" / "StudySandbox"
    
    engine = StudySyncEngine(target_dir=safe_target)
    engine.organize()