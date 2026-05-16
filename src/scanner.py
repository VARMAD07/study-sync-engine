import PyPDF2
from pathlib import Path
from PIL import Image
import pytesseract

class DocumentScanner:
    def __init__(self):
        # Explicitly pointing Python to your Windows Tesseract installation path
        # If you installed Tesseract to a custom path, update this string!
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        # The intelligence matrix
        self.knowledge_base = {
            "Academics/Physics": ["thermodynamics", "kinematics", "velocity", "quantum", "optics", "magnetic", "jee physics", "force", "acceleration"],
            "Academics/Math": ["calculus", "algebra", "integration", "theorem", "matrix", "probability", "jee math", "derivative", "function"],
            "Academics/Chemistry": ["organic", "inorganic", "mole", "titration", "orbital", "polymer", "jee chemistry", "reaction", "acid", "base"],
            "Language/Japanese": ["kanji", "hiragana", "katakana", "jlpt", "vocabulary", "grammar", "particles", "nihongo", "日本語"]
        }

    def scan_pdf(self, file_path):
        """Extracts text strings from a PDF document."""
        text_content = ""
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                pages_to_scan = min(3, len(reader.pages))
                for i in range(pages_to_scan):
                    page = reader.pages[i]
                    text_content += page.extract_text().lower()
        except Exception:
            return None
        return self._analyze_text(text_content)

    def scan_image(self, file_path):
        """Extracts text content from images using simultaneous English + Japanese OCR."""
        try:
            img = Image.open(file_path)
            
            # --- THE MULTILINGUAL UPGRADE ---
            # 'eng+jpn' tells Tesseract to scan the pixel layout for both alphabets at the same time
            text_content = pytesseract.image_to_string(img, lang="eng+jpn").lower()
            
            return self._analyze_text(text_content)
        except Exception as e:
            print(f"[SCANNER ERROR] Image processing skipped: {str(e)}")
            return None
        
    def _analyze_text(self, text):
        """Scores the text against our knowledge base to find the best match."""
        if not text.strip():
            return None
            
        scores = {category: 0 for category in self.knowledge_base}
        
        for category, keywords in self.knowledge_base.items():
            for word in keywords:
                scores[category] += text.count(word)
                
        best_match = max(scores, key=scores.get)
        
        if scores[best_match] > 0:
            return best_match
        return None