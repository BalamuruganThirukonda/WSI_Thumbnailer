import os
import platform
import ctypes
from pathlib import Path

def load_openslide(openslide_dll_path):

    if platform.system() == "Windows" and hasattr(os, "add_dll_directory"):

        if os.path.exists(openslide_dll_path):

            os.environ["PATH"] = openslide_dll_path + os.pathsep + os.environ.get("PATH", "")

            with os.add_dll_directory(openslide_dll_path):
                ctypes.cdll.LoadLibrary(str(Path(openslide_dll_path) / "libopenslide-0.dll"))