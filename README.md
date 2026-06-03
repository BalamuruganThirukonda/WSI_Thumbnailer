# WSI Thumbnailer Pipeline

This project automatically processes Whole Slide Images (WSI) by generating thumbnails and optionally deleting old files.

---

## 🚀 Features

- Automatic thumbnail generation for WSI files
- Folder monitoring (real-time + scan on startup)
- Recursive folder support
- Exclude specific folders (e.g., "failed")
- Auto deletion of old slides
- SQLite database tracking (optional)

---

## 📂 Supported File Types

- .svs
- .tif
- .ndpi
- .mrxs
- .vms

---

## ⚙️ Configuration

All pipeline behavior is controlled in `config.py`.

### Example:

```python
WATCH_FOLDERS = [
    {
        "path": "D:/Slides/CaseSlides",
        "handler": "thumbnail_on_create",
        "output_dir": "D:/Slides/Thumbnails",
        "exclude_folders": ["failed"]
    },
    {
        "path": "D:/Slides/SectraImport",
        "handler": "delete_if_older_than",
        "days": 10
    }
]