from config import WATCH_FOLDERS
from watcher import start_watchers
from handlers.thumbnail_handler import scan_folder, delete_if_older_than


print("\n--- Processing existing files ---")

for folder in WATCH_FOLDERS:

    path = folder["path"]
    handler = folder["handler"]

    # Only run scan if handler exists
    if handler:
        kwargs = {
            k: v for k, v in folder.items()
            if k not in ["path", "handler", "delete_after_days"]
        }

        scan_folder(path, handler, **kwargs)

    # Always run deletion if configured
    if "delete_after_days" in folder:

        delete_if_older_than(path, folder["delete_after_days"])


print("\n--- Starting watchers ---")

start_watchers(WATCH_FOLDERS)