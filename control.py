import os
from datetime import datetime
import tkinter as tk
from PIL import ImageGrab

class ControlPanel:
    BG      = "#12121f"
    BTN_SAV = "#0d7fcc"
    BTN_HOV = "#0a6aab"
    BTN_EXT = "#2a2a3e"
    BTN_EHV = "#3a3a55"
    FG      = "#e0eeff"

    def __init__(self, root, selector):
        self.root     = root
        self.selector = selector

        self.win = tk.Toplevel(root)
        self.win.title("Capture Controls")
        self.win.resizable(False, False)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=self.BG)
        self.win.protocol("WM_DELETE_WINDOW", self._exit)

        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        pw, ph = 640, 360
        self.win.geometry(f"{pw}x{ph}+{(sw-pw)//2}+{sh-ph-60}")

        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self.win,
            text="Screen Region Capture",
            font=("Helvetica", 11, "bold"),
            fg=self.FG,
            bg=self.BG,
        ).pack(pady=(14, 2))

        tk.Label(
            self.win,
            text="Position and resize the blue border, then capture.",
            font=("Helvetica", 8),
            fg="#6688aa",
            bg=self.BG,
        ).pack()

        btn_frame = tk.Frame(self.win, bg=self.BG)
        btn_frame.pack(pady=10)

        self.save_btn = tk.Button(
            btn_frame,
            text="  📷  Save Screenshot",
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg=self.BTN_SAV,
            activebackground=self.BTN_HOV,
            activeforeground="white",
            relief="flat",
            padx=18, pady=7,
            cursor="hand2",
            command=self._save,
        )
        self.save_btn.pack()
        self.save_btn.bind("<Enter>", lambda e: self.save_btn.configure(bg=self.BTN_HOV))
        self.save_btn.bind("<Leave>", lambda e: self.save_btn.configure(bg=self.BTN_SAV))

        self.status_lbl = tk.Label(
            self.win, text="",
            font=("Helvetica", 8),
            fg="#00cc77", bg=self.BG,
        )
        self.status_lbl.pack()

    # ── actions ──────────────────────────────────────────────────────────────
    def _save(self):
        region = self.selector.get_region()

        # Hide both windows so they don't appear in the shot
        self.selector.root.withdraw()
        self.win.withdraw()
        self.win.update()

        try:
            screenshot = ImageGrab.grab(bbox=region)
            ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{ts}.png"
            screenshot.save(filename)
            abs_path = os.path.abspath(filename)
            self.selector.flash(f"✓ Saved  {filename}")
            self._set_status(f"✓ Saved: {filename}", ok=True)
            print(f"Saved: {abs_path}  (region {region}, scale {self.selector.scale:.2f}×)")
        except Exception as exc:
            self.selector.flash(f"✗ Error: {exc}", colour="#ff5555")
            self._set_status(f"✗ {exc}", ok=False)
            print(f"Error: {exc}")
        finally:
            self.selector.root.deiconify()
            self.selector.root.attributes("-topmost", True)
            self.win.deiconify()
            self.win.attributes("-topmost", True)

    def _exit(self):
        self.root.quit()

    def _set_status(self, msg, ok=True):
        self.status_lbl.configure(text=msg, fg="#00cc77" if ok else "#ff5555")
        self.win.after(4000, lambda: self.status_lbl.configure(text=""))