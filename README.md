# StudySyncEngine 🚀

An automation-driven, context-aware academic workspace organizer and focus environment built from scratch in Python. It utilizes multi-threaded file monitoring, an asynchronous pub/sub event broker, and computer vision (OCR) parsing pipelines to categorize desktop clutter dynamically while protecting your attention span.

---

## 🛠️ Deep Systems Architecture

### 1. Asynchronous Multithreading & Messaging Engine
To prevent UI-blocking frame dropouts during heavy indexing loads, `StudySyncEngine` isolates compute-heavy operations onto detached execution streams. Communication between core backend components and the UI layer is decoupled using a native **Singleton Event Message Broker (Pub/Sub)** pattern, broadcasting processing logs smoothly in real-time.

### 2. Multi-Modal Optical Classification Channels
Standard extensions aren't enough. The processing engine features context-aware pipelines to read the actual content of documents before choosing a folder destination:
* **Text Dimension:** Integrates standard file scanners to extract structural string markers from complex multi-page PDFs.
* **Vision Dimension:** Leverages an **Optical Character Recognition (OCR)** engine powered by Tesseract to analyze text layouts hidden directly inside raw image pixels (`.png`, `.jpg`).
* **Multilingual Fallback:** Simultaneously scans graphic layouts for English technical concepts and Japanese characters (Kanji, Hiragana, Katakana).

### 3. Automated File Warden (`watchdog`)
Enaging the file warden hooks directly into native Windows OS filesystem event channels. The second an assignment, lecture deck, or file drops into your monitored directory, the background tracker intercepts the drop event and processes it instantly.

### 4. Process-Terminating Focus Guard & Persistence Ledger
Features a rigid commitment lockdown state that dynamically re-morphs the UI workspace layout, blocking active controls and tracking study cycles. The guard loops monitor system process tables to aggressively terminate distracting applications (`.exe`), saving your daily metrics into a local database ledger.

---

## 🗂️ Core Ecosystem Structure

```text
study-sync-engine/
│
├── src/
│   ├── main.py              # Main application entry vector
│   ├── gui.py               # Modern Treeview Tkinter Dashboard UI
│   ├── engine.py            # File system operational mechanics & I/O
│   ├── scanner.py           # Multi-Modal PDF Parser & Tesseract OCR Matrix
│   ├── watcher.py           # Background Windows Watchdog Listener
│   ├── broker.py            # Pub/Sub Singleton Event Router
│   ├── focus.py             # Process-terminating Focus Guard loop
│   ├── stats.py             # Analytics persistence tracker
│   └── logger.py            # Diagnostic crash-dump log reporter
│
├── config.json              # Dynamic taxonomy mapping schemas
├── requirements.txt         # Package dependency blueprint
└── StudySyncEngine.spec     # Automated PyInstaller compilation parameters