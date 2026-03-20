#!/usr/bin/env python3
"""
Screen Region Capture Tool
- Displays a resizable, draggable border overlay on screen
- A separate control panel provides Save and Exit buttons
"""

import sys
import os
import tkinter as tk
from capture import RegionSelector
from control import ControlPanel

try:
    from PIL import ImageGrab
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

def main():
    if not HAS_DEPS:
        import subprocess
        print("Installing Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--quiet"])
        from PIL import ImageGrab  # noqa: F401

    scale = 1.0  # default win32 scale with DPI awareness
    if sys.platform == "win32":
        from ctypes import windll
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            print("Failed to set DPI awareness")
            pass
        
    print(f"Scale: {scale}")

    root = tk.Tk()
    root.withdraw()

    selector = RegionSelector(tk.Toplevel(root), scale)
    ControlPanel(root, selector)

    root.mainloop()


if __name__ == "__main__":
    main()