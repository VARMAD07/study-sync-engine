import json
from pathlib import Path

class StatsManager:
    def __init__(self):
        self.filepath = Path(__file__).parent / "stats.json"
        self.stats = self.load_stats()

    def load_stats(self):
        """Loads your lifetime stats from disk."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # If it's your first time, create a blank slate
            default_stats = {
                "total_focus_minutes": 0, 
                "distractions_killed": 0, 
                "sessions_completed": 0
            }
            self.save_stats(default_stats)
            return default_stats

    def save_stats(self, data=None):
        """Saves your stats securely."""
        if data is None:
            data = self.stats
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def log_session(self, minutes, kills):
        """Updates the ledger after a successful focus session."""
        self.stats["total_focus_minutes"] += minutes
        self.stats["distractions_killed"] += kills
        self.stats["sessions_completed"] += 1
        self.save_stats()