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
        try:
            self.handler(file_path, **self.kwargs)
        except Exception as e:
            print(f"[ERROR] {file_path} | {e}")

def start_watchers(config):
    observer = Observer()
    for folder in config:
        path = folder["path"]
        handler = folder["handler"]

        # Skip folders without handler
        if hander is None:
            continue

        kwargs = {k: v for k, v in folder.items() if k not in ["path", "handler", "delete_after_days"]}
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
