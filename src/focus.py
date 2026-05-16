import os
import platform

class FocusMode:
    def __init__(self):
        # The hit-list. You can add any other games or apps that distract you here.
        self.distractions = [
            "discord.exe",
            "steam.exe",
            "spotify.exe",
            "epicgameslauncher.exe",
            "whatsapp.exe"
        ]

    def engage(self):
        """Hunts down and terminates distraction processes."""
        if platform.system() != "Windows":
            return ["⚠️ Focus Mode currently only supports Windows."]
        
        log = []
        for app in self.distractions:
            # We command Windows to forcibly kill the process by its image name
            # >nul 2>&1 just hides the messy Windows terminal output
            result = os.system(f"taskkill /f /im {app} /t >nul 2>&1")
            
            # taskkill returns 0 if it successfully assassinated the target
            if result == 0:
                log.append(f"🛑 Terminated: {app}")
                
        if not log:
            log.append("✨ No distractions found. Your environment is clean.")
            
        return log