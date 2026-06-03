import os
import time
from datetime import datetime, timedelta
from PIL import Image
import openslide

# Supported WSI file extensions
WSI_EXTS = (".svs", ".tif", ".ndpi", ".mrxs", ".vms")


# -----------------------------
# Wait until file copy finishes
# -----------------------------
def wait_until_file_ready(file_path, check_interval=5):
    """
    Wait until the file copy is complete by monitoring its size.

    Args:
        file_path (str): Path to the file being copied.
        check_interval (int): Time in seconds between size checks.

    Returns:
        bool: True if file is ready, False if file does not exist.
    """
    size_previous = -1
    while True:
        if not os.path.exists(file_path):
            return False
        size_current = os.path.getsize(file_path)
        if size_current == size_previous:
            return True
        size_previous = size_current
        time.sleep(check_interval)


# -----------------------------
# Create a WSI thumbnail
# -----------------------------
def save_wsi_thumbnail(wsi_path, output_dir, thumb_size=1024):
    """
    Generate a thumbnail for a given WSI file and return metadata.

    Args:
        wsi_path (str): Path to the WSI file.
        output_dir (str): Folder to save the thumbnail.
        thumb_size (int): Maximum width/height of the thumbnail.

    Returns:
        tuple: (thumbnail_path, level_used, width, height) or (None, None, None, None) on error.
    """
    fname = os.path.basename(wsi_path)
    thumb_name = os.path.splitext(fname)[0] + "_thumb.jpg"
    output_path = os.path.join(output_dir, thumb_name)

    # If thumbnail already exists, return metadata
    if os.path.exists(output_path):
        print(f"[SKIP] Thumbnail already exists: {thumb_name}")
        try:
            slide = openslide.OpenSlide(wsi_path)
            level = min(2, slide.level_count - 1)
            w, h = slide.level_dimensions[level]
            return output_path, level, w, h
        except:
            return output_path, None, None, None

    try:
        slide = openslide.OpenSlide(wsi_path)
        level = min(2, slide.level_count - 1)
        w, h = slide.level_dimensions[level]
        scale = thumb_size / max(w, h)
        new_w, new_h = int(w * scale), int(h * scale)
        thumb = slide.read_region((0, 0), level, (w, h)).convert("RGB")
        thumb = thumb.resize((new_w, new_h), Image.LANCZOS)
        os.makedirs(output_dir, exist_ok=True)
        thumb.save(output_path, quality=90)
        print(f"[OK] Thumbnail saved: {output_path}")
        return output_path, level, w, h
    except Exception as e:
        print(f"[ERROR] Failed to create thumbnail for {wsi_path}: {e}")
        return None, None, None, None


# -----------------------------
# Handler: create thumbnail on new WSI
# -----------------------------
def thumbnail_on_create(file_path, output_dir, thumb_size=1024):
    """
    Handler function to create a thumbnail for new WSI files
    and insert metadata into the database.

    Args:
        file_path (str): Path to the WSI file.
        output_dir (str): Folder to save the thumbnail.
        thumb_size (int): Maximum width/height of the thumbnail.

    Returns:
        None
    """
    from utils.database import slide_exists, insert_slide

    if not file_path.lower().endswith(WSI_EXTS):
        return
    if not os.path.exists(file_path):
        return
    if slide_exists(file_path):
        print(f"[SKIP] Already processed: {file_path}")
        return

    print(f"[NEW FILE] {file_path}")
    wait_until_file_ready(file_path)
    thumb_path, level, width, height = save_wsi_thumbnail(file_path, output_dir, thumb_size)
    if thumb_path:
        insert_slide(
            wsi_path=file_path,
            thumbnail_path=thumb_path,
            level_used=level,
            width=width,
            height=height
        )


# -----------------------------
# Scan existing folder for WSI files
# -----------------------------
def scan_folder(folder_path, handler, **kwargs):
    """
    Scan a folder recursively and apply a handler to each WSI file.

    Args:
        folder_path (str): Folder to scan.
        handler (function): Function to handle each WSI file.
        **kwargs: Additional keyword arguments for the handler.

    Returns:
        None
    """
    print(f"[SCAN] Checking folder: {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not file_path.lower().endswith(WSI_EXTS):
                continue
            try:
                handler(file_path, **kwargs)
            except Exception as e:
                print(f"[ERROR] {file_path} | {e}")


# -----------------------------
# Delete old WSI files and optionally thumbnails
# -----------------------------
def delete_if_older_than(folder_path, days=10, delete_thumbnails=False, thumbnail_folder=None):
    """
    Delete WSI files older than specified days. Optionally delete corresponding thumbnails.

    Args:
        folder_path (str): Folder containing WSI files.
        days (int): Age in days to trigger deletion.
        delete_thumbnails (bool): Whether to delete thumbnails as well.
        thumbnail_folder (str): Folder where thumbnails are stored.

    Returns:
        None
    """
    print(f"[CLEANUP] Checking files older than {days} days in {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not file_path.lower().endswith(WSI_EXTS):
                continue
            if not os.path.exists(file_path):
                continue
            creation_time = os.path.getctime(file_path)
            file_date = datetime.fromtimestamp(creation_time)
            if datetime.now() - file_date > timedelta(days=days):
                try:
                    os.remove(file_path)
                    print(f"[DELETE] {file_path}")

                    # Delete thumbnail if requested
                    if delete_thumbnails and thumbnail_folder:
                        thumb_name = os.path.splitext(file)[0] + "_thumb.jpg"
                        thumb_path = os.path.join(thumbnail_folder, thumb_name)
                        if os.path.exists(thumb_path):
                            os.remove(thumb_path)
                            print(f"[DELETE] Thumbnail {thumb_path}")

                except Exception as e:
                    print(f"[ERROR] Could not delete {file_path}: {e}")