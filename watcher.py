import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
WSI_EXTS = (".svs", ".tif", ".ndpi", ".mrxs", ".vms")

class FolderHandler(FileSystemEventHandler):
    def __init__(self, handler, kwargs):
        self.handler = handler
        self.kwargs = kwargs

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        if not file_path.lower().endswith(WSI_EXTS):
            return

        # -----------------------------
        # Exclude folders (FAILED, etc.)
        # -----------------------------
        exclude_folders = [
            f.lower() for f in self.kwargs.get("exclude_folders", [])
        ]

        file_parts = [p.lower() for p in file_path.split(os.sep)]

        if any(folder in part for folder in exclude_folders for part in file_parts):
            return

        try:
            # IMPORTANT: remove exclude_folders before sending to handler
            clean_kwargs = {
                k: v for k, v in self.kwargs.items()
                if k != "exclude_folders"
            }

            self.handler(file_path, **clean_kwargs)

        except Exception as e:
            print(f"[ERROR] {file_path} | {e}")


def start_watchers(config):

    observer = Observer()

    for folder in config:

        path = folder["path"]
        handler = folder["handler"]

        # Skip folders without handler
        if handler is None:
            continue

        kwargs = {
            k: v for k, v in folder.items()
            if k not in ["path", "handler", "delete_after_days"]
        }

        event_handler = FolderHandler(handler, kwargs)
        observer.schedule(event_handler, path, recursive=True)

        print(f"[WATCHING] {path}")

    observer.start()

    try:
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
