import os
import traceback
from datetime import datetime
from pathlib import Path

class CrashLogger:
    def __init__(self):
        self.log_dir = Path(__file__).parent.parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "system_runtime.log"

    def log_exception(self, context_message, exception_object):
        """Captures the absolute error string, timestamp, and line number failure."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stack_trace = traceback.format_exc()
        
        log_payload = (
            f"==================================================\n"
            f"TIMESTAMP: {timestamp}\n"
            f"CONTEXT: {context_message}\n"
            f"ERROR: {str(exception_object)}\n"
            f"--------------------------------------------------\n"
            f"STACK TRACE:\n{stack_trace}"
            f"==================================================\n\n"
        )
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_payload)
            print(f"[LOGGER CRITICAL] Exception dumped cleanly to {self.log_file}")
        except Exception as logger_fail:
            print(f"Fatal error write failure: {str(logger_fail)}")