"""
StudySyncEngine - Core Application Vector
Author: Mohammad Hammad Faridi
Session: 2026-2027

This module serves as the primary runtime entry point for the application. 
It instantiates the Tkinter loop environment, maps core styling vectors, 
and safely initializes our asynchronous background services.
"""

import tkinter as tk
import sys
from pathlib import Path

# Fix path resolution mapping when running as a compiled standalone binary (.exe)
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from gui import StudySyncUI
from logger import CrashLogger

def main():
    """
    Initializes the system framework context, loads the master UI layout,
    and runs the global application loop handles safely.
    """
    # Instantiate our enterprise crash dumper to catch any unhandled boot exceptions
    sys_logger = CrashLogger()
    
    try:
        # Initialize primary Tkinter window structure
        root = tk.Tk()
        
        # Enforce dark theme style maps and geometries
        root.configure(bg="#1E1E1E")
        
        # Spin up our primary layout controller interface
        app = StudySyncUI(root)
        
        # Hand processing loop constraints over to the native OS window manager
        root.mainloop()
        
    except Exception as boot_error:
        # If the window fails to mount or an external asset is locked, dump diagnostics instantly
        sys_logger.log_exception("Fatal runtime crash during system boot layout phase", boot_error)
        print(f"[FATAL BOOT ENGINE ERROR] Crash dump successfully recorded. Context: {str(boot_error)}")
        sys.exit(1)

if __name__ == "__main__":
    main()