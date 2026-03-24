#!/usr/bin/env python3
"""
Screen Region Translater
- Displays a resizable, draggable border overlay on screen to control capture region.
- Separate window for screen capture and translation output.
"""

import sys
import tkinter as tk
from loguru import logger
from capture import RegionSelector
from control import ControlPanel
from ocr import ocr
from deepltranslate import translater

def main():
    scale = 1.0  # default win32 scale with DPI awareness
    if sys.platform == "win32":
        from ctypes import windll
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            logger.error("Failed to set DPI awareness.")
            pass
        
    logger.info(f"Scale: {scale}")

    root = tk.Tk()
    root.withdraw()

    reader = ocr()
    tl = translater()
    selector = RegionSelector(tk.Toplevel(root), scale)
    ControlPanel(root, selector, reader, tl)

    root.mainloop()

if __name__ == "__main__":
    main()