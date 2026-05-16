import json
from pathlib import Path
from PIL import Image
import PyPDF2
import pytesseract

class DocumentScanner:
    def __init__(self):
        self.config_path = Path(__file__).parent / "config.json"
        self.load_dynamic_settings()

    def load_dynamic_settings(self):
        """Loads Tesseract paths and keywords dynamically to ensure cross-platform portability."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Dynamically assign the system pointer from config
            pytesseract.pytesseract.tesseract_cmd = config.get("tesseract_path", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
            self.knowledge_base = config.get("keywords", {})
        except Exception:
            # Safe local fallbacks if the config is temporarily corrupted
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            self.knowledge_base = {}

    def scan_pdf(self, file_path):
        """Extracts text strings from a PDF document."""
        self.load_dynamic_settings() # Hot-reload keywords if changed in GUI
        text_content = ""
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                pages_to_scan = min(3, len(reader.pages))
                for i in range(pages_to_scan):
                    text_content += reader.pages[i].extract_text().lower()
        except Exception:
            return None
        return self._analyze_text(text_content)

    def scan_image(self, file_path):
        """Extracts text content from images using simultaneous multilingual OCR."""
        self.load_dynamic_settings()
        try:
            img = Image.open(file_path)
            text_content = pytesseract.image_to_string(img, lang="eng+jpn").lower()
            return self._analyze_text(text_content)
        except Exception:
            return None

    def _analyze_text(self, text):
        """Scores text against dynamic keyword maps to resolve destination folder categories."""
        if not text.strip() or not self.knowledge_base:
            return None
            
        scores = {category: 0 for category in self.knowledge_base}
        for category, keywords in self.knowledge_base.items():
            for word in keywords:
                scores[category] += text.count(word)
                
        best_match = max(scores, key=scores.get)
        if scores[best_match] > 0:
            return best_match
        return None