import os
import platform
import json
from pathlib import Path

class FocusMode:
    def __init__(self):
        self.config_path = Path(__file__).parent / "hitlist.json"
        self.load_hitlist()

    def load_hitlist(self):
        """Loads the hitlist. Now uses a modern dictionary format."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.distractions = json.load(f)
        except FileNotFoundError:
            # New format: "Clean Name": {"exe": "file.exe", "active": True/False}
            self.distractions = {
                "Discord": {"exe": "discord.exe", "active": True},
                "Steam": {"exe": "steam.exe", "active": True},
                "Spotify": {"exe": "spotify.exe", "active": False},
                "WhatsApp": {"exe": "whatsapp.exe", "active": True},
                "Epic Games": {"exe": "epicgameslauncher.exe", "active": True}
            }
            self.save_hitlist()

    def save_hitlist(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.distractions, f, indent=4)

    def engage(self, silent=False):
        if platform.system() != "Windows":
            return ["⚠️ Focus Mode currently only supports Windows."]
        
        self.load_hitlist()
        log = []
        
        for app_name, data in self.distractions.items():
            if data["active"]:
                exe_name = data["exe"]
                result = os.system(f"taskkill /f /im {exe_name} /t >nul 2>&1")
                if result == 0:
                    # Log the clean name, not the exe
                    log.append(f"🛑 Snipped: {app_name}")
                    
        if not log and not silent:
            log.append("✨ No distractions found. Environment clean.")
            
        return log