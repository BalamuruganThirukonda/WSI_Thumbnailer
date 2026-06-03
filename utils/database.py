import sqlite3
from datetime import datetime
import os

DB_PATH = "WSIThumbnailer.db"

# -----------------------------
# Initialize DB
# -----------------------------
def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS slides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wsi_path TEXT UNIQUE,
            thumbnail_path TEXT,
            created_at TIMESTAMP,
            status TEXT DEFAULT 'processed',
            original_size INTEGER,
            slide_name TEXT,
            level_used INTEGER,
            width INTEGER,
            height INTEGER
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Check if WSI already processed
# -----------------------------
def slide_exists(wsi_path, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT 1 FROM slides WHERE wsi_path = ?", (wsi_path,))
    result = c.fetchone()
    conn.close()
    return result is not None

# -----------------------------
# Insert new slide metadata
# -----------------------------
def insert_slide(wsi_path, thumbnail_path, db_path=DB_PATH,
                 status="processed", original_size=None, slide_name=None,
                 level_used=None, width=None, height=None):

    if original_size is None:
        try:
            original_size = os.path.getsize(wsi_path)
        except:
            original_size = None
    if slide_name is None:
        slide_name = os.path.basename(wsi_path)

    created_at = datetime.now()

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO slides (
            wsi_path, thumbnail_path, created_at, status,
            original_size, slide_name, level_used, width, height
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (wsi_path, thumbnail_path, created_at, status,
          original_size, slide_name, level_used, width, height))
    conn.commit()
    conn.close()

# Initialize DB
init_db()