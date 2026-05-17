# StudySyncEngine 🚀

StudySyncEngine is a Python-based desktop workspace organizer designed for students managing large amounts of study material and digital clutter.

The application monitors folders in real time, analyzes incoming files using text extraction and OCR, and automatically organizes documents into subject-based directories. It also includes a lightweight focus mode that helps reduce distractions during study sessions.

The goal of the project is simple: reduce friction in digital study environments and make academic workflows easier to manage.

---

## Features

- Real-time folder monitoring using Watchdog
- OCR support for scanned notes and image-based documents
- Automatic subject-wise file organization
- Lightweight focus mode for reducing distractions
- Local study statistics tracking
- Modular event-driven architecture

---

## Architecture

```text
Watchdog → Scanner → Broker → Engine → UI
                     ↓
                 Focus Guard
```

---

## Project Structure

```text
study-sync-engine/
│
├── src/
│   ├── main.py            # Application entry point
│   ├── gui.py             # Tkinter dashboard interface
│   ├── engine.py          # File organization engine
│   ├── scanner.py         # Text extraction and OCR pipeline
│   ├── watcher.py         # Real-time filesystem monitoring
│   ├── broker.py          # Event messaging system
│   ├── focus.py           # Focus mode process controller
│   ├── stats.py           # Study statistics tracker
│   └── logger.py          # Logging and diagnostics
│
├── tests/                 # Test modules
├── requirements.txt       # Project dependencies
├── config.json            # File categorization rules
├── .gitignore
├── .gitattributes
└── README.md
```

---

## Installation

```bash
git clone https://github.com/VARMAD07/study-sync-engine.git
cd study-sync-engine
pip install -r requirements.txt
python src/main.py
```

---

## Example Workflow

1. A lecture PDF or image is added to the monitored folder
2. Watchdog detects the new filesystem event
3. Text extraction or OCR scanning begins
4. Keywords are matched against configured subject rules
5. The file is moved into its matching directory
6. Study statistics are updated locally

---

## Design Decisions

- Tkinter was chosen to keep the application lightweight and easy to run locally.
- OCR support was added because many lecture notes are image-based scans rather than searchable PDFs.
- The pub/sub broker was introduced after direct UI updates started causing interface freezes during larger scans.
- Watchdog allows the engine to react instantly to filesystem events without requiring manual refreshes.

---

## Current Limitations

- OCR accuracy depends heavily on image quality
- Currently optimized for Windows systems
- Large batch scans may temporarily slow the interface

---

## Future Improvements

- Semantic document classification
- Cloud synchronization support
- Cross-device session persistence
- Improved OCR accuracy for handwritten notes
- Expanded analytics and productivity tracking

---

## License

This project is currently intended for educational and personal use.
