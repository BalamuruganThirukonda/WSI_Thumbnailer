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
```


## 🔧 Available Handlers

| Handler Name         | Description                         |
| -------------------- | ----------------------------------- |
| thumbnail_on_create  | Creates thumbnail for new WSI files |
| delete_if_older_than | Deletes old WSI files after N days  |


## 📁 Folder Options
| Key             | Description                |
| --------------- | -------------------------- |
| path            | Folder to watch            |
| handler         | Function name (string)     |
| output_dir      | Thumbnail output folder    |
| exclude_folders | Folders to ignore          |
| days            | Age threshold for deletion |


## ▶️ How to Run

### Windows (recommended)

```bash
python main.py
```

or run .bat file:
run_thumbnailer.bat

## ⚠️ Notes
- Always ensure OpenSlide is installed correctly
- Use recursive=True if processing subfolders
- Avoid placing files in "failed" folders (if excluded)

