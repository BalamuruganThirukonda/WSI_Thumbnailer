from handlers.thumbnail_handler import thumbnail_on_create, delete_if_older_than

WATCH_FOLDERS = [
    # -------------------------------------------------------------
    # ScanHub
    # -------------------------------------------------------------
    # This folder receives incoming WSI files.
    # Thumbnails will be created immediately when files appear.
    # The original WSI files will NOT be deleted automatically.
    {
        "path": "/home/thirukondabalamurugan/Desktop/CPHGPU1-Slides/ScanHub",
        "handler": thumbnail_on_create,
        "output_dir": "/home/thirukondabalamurugan/Desktop/CPHGPU1-Slides/Thumbnails"
    },
    # -------------------------------------------------------------
    # CaseSlides
    # -------------------------------------------------------------
    # This folder contains slides that should be archived.
    # A thumbnail will be generated for each WSI file.
    # After 10 days the original WSI file will be deleted automatically.
    {
        "path": "/home/thirukondabalamurugan/Desktop/CPHGPU1-Slides/CaseSlides",
        "handler": thumbnail_on_create,
        "output_dir": "/home/thirukondabalamurugan/Desktop/CPHGPU1-Slides/Thumbnails",
        "delete_after_days": 10
    },

    # -------------------------------------------------------------
    # SectraImport
    # -------------------------------------------------------------
    # This folder contains slides that should be removed after 10 days.
    {
        "path": "/home/thirukondabalamurugan/Desktop/CPHGPU1-Slides/SectraImport",
        "handler": None,
        "delete_after_days": 10
    }
]
