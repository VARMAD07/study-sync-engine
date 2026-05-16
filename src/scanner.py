import PyPDF2
from pathlib import Path

class DocumentScanner:
    def __init__(self):
        # The intelligence matrix. You can add more keywords later.
        self.knowledge_base = {
            "Academics/Physics": ["thermodynamics", "kinematics", "velocity", "quantum", "optics", "magnetic", "jee physics"],
            "Academics/Math": ["calculus", "algebra", "integration", "theorem", "matrix", "probability", "jee math"],
            "Academics/Chemistry": ["organic", "inorganic", "mole", "titration", "orbital", "polymer", "jee chemistry"],
            "Language/Japanese": ["kanji", "hiragana", "katakana", "jlpt", "vocabulary", "grammar", "particles", "nihongo"]
        }

    def scan_pdf(self, file_path):
        """Opens a PDF, reads the first 3 pages, and categorizes it based on keywords."""
        text_content = ""
        
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                # Read up to the first 3 pages to figure out what it is
                pages_to_scan = min(3, len(reader.pages))
                
                for i in range(pages_to_scan):
                    page = reader.pages[i]
                    text_content += page.extract_text().lower()
                    
        except Exception as e:
            return None # If the PDF is locked or corrupted, return None

        return self._analyze_text(text_content)

    def _analyze_text(self, text):
        """Scores the text against our knowledge base to find the best match."""
        scores = {category: 0 for category in self.knowledge_base}
        
        # Count how many times our keywords appear in the document
        for category, keywords in self.knowledge_base.items():
            for word in keywords:
                scores[category] += text.count(word)
                
        # Find the category with the highest score
        best_match = max(scores, key=scores.get)
        
        # Only return the category if we actually found keywords (score > 0)
        if scores[best_match] > 0:
            return best_match
        
        return "Academics/General" # Fallback if we can't figure it out