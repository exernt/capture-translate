import os
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageGrab
from loguru import logger

class ControlPanel:
    BG      = "#b8b8b8"
    BTN_SAV = "#0d7fcc"
    BTN_HOV = "#0a6aab"
    saved_context = []

    def __init__(self, root, selector, ocr, tl):
        self.root = root
        self.selector = selector
        self.ocr = ocr
        self.tl = tl

        self.win = tk.Toplevel(root)
        self.win.title("Capture Controls")
        self.win.resizable(False, False)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=self.BG)
        self.win.protocol("WM_DELETE_WINDOW", self._exit)

        self.output_var = tk.StringVar(self.win)

        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        pw, ph = 1024, 768
        self.win.geometry(f"{pw}x{ph}+{(sw-pw)//2}+{sh-ph-120}")

        self._build_ui()

    def _build_ui(self):
        # title
        tk.Label(
            self.win,
            text="Screen Region Translater",
            font=("Helvetica", 15, "bold"),
            fg="black",
            bg=self.BG,
        ).pack(pady=(14, 2))

        # subtitle
        tk.Label(
            self.win,
            text="Position and resize the blue border, then capture.",
            font=("Helvetica", 10),
            fg="black",
            bg=self.BG,
        ).pack()

        # output text region
        self.text_area = scrolledtext.ScrolledText(
            self.win,
            wrap=tk.WORD,
            font=("Helvetica", 15),
            width=50,
            height=14,
            state='disabled'
        )
        self.text_area.pack(pady=10)

        btn_frame = tk.Frame(self.win, bg=self.BG)
        btn_frame.pack(pady=10, side=tk.TOP)
        # save button
        self.save_btn = tk.Button(
            btn_frame,
            text="Capture",
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg=self.BTN_SAV,
            activebackground=self.BTN_HOV,
            activeforeground="white",
            relief="flat",
            padx=18, pady=7,
            cursor="hand2",
            command=self._capture,
        )
        self.save_btn.pack(padx=10, side=tk.LEFT)
        self.save_btn.bind("<Enter>", lambda e: self.save_btn.configure(bg=self.BTN_HOV))
        self.save_btn.bind("<Leave>", lambda e: self.save_btn.configure(bg=self.BTN_SAV))

        # reset button
        self.reset_btn = tk.Button(
            btn_frame,
            text="Reset Text",
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg=self.BTN_SAV,
            activebackground=self.BTN_HOV,
            activeforeground="white",
            relief="flat",
            padx=18, pady=7,
            cursor="hand2",
            command=self._reset_text
        )
        self.reset_btn.pack(side=tk.LEFT)
        self.reset_btn.bind("<Enter>", lambda e: self.save_btn.configure(bg=self.BTN_HOV))
        self.reset_btn.bind("<Leave>", lambda e: self.save_btn.configure(bg=self.BTN_SAV))

        self.status_lbl = tk.Label(
            self.win, 
            text="",
            font=("Helvetica", 10),
            fg="black", bg=self.BG
        )
        self.status_lbl.pack()

    # ── actions ──────────────────────────────────────────────────────────────
    @logger.catch
    def _capture(self):
        region = self.selector.get_region()

        # hides overlay so it does not appear in shot
        self.selector.root.withdraw()
        self.selector.root.update()

        try:
            screenshot = ImageGrab.grab(bbox=region)
            filename = "capture.png"
            screenshot.save(filename)
            abs_path = os.path.abspath(filename)
            self._set_status("Capture Successful", ok=True)
            logger.info(f"Saved: {abs_path}  (region {region}, scale {self.selector.scale:.2f}×)")

            path = "./" + filename
            text = self.ocr.readImage(path)
            self.saved_context.append(text)
            tl_result = self.tl.translate(text, self.saved_context)
            self.text_area.configure(state="normal")
            self.text_area.insert(tk.END, text + "\n" + tl_result.text + "\n")
            self.text_area.configure(state="disabled")
            logger.info(f"Read: {text}")
            logger.info(f"Translated to: {tl_result.text}")

        except Exception as exc:
            #self.selector.flash(f"✗ Error: {exc}", colour="#ff5555")
            self._set_status(f"✗ {exc}", ok=False)
            logger.exception(f"Error: {exc}")
        finally:
            self.selector.root.deiconify()
            self.selector.root.attributes("-topmost", True)

    def _exit(self):
        self.root.quit()

    def _set_status(self, msg, ok=True):
        self.status_lbl.configure(text=msg, fg="black")
        self.win.after(4000, lambda: self.status_lbl.configure(text=""))

    def _reset_text(self):
        self.saved_context.clear()
        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, tk.END)
        self.text_area.configure(state="disabled")