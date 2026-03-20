import tkinter as tk

class RegionSelector:
    BORDER   = 1
    HANDLE   = 14
    MIN_SIZE = 80
    ACCENT   = "#00aaff"
    BG       = "#1a1a2e"

    def __init__(self, root, scale):
        self.root  = root
        self.scale = scale          # physical pixels per logical pixel

        self.root.title("Capture Region")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.2)
        self.root.overrideredirect(True)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 520, 360
        x, y = (sw - w) // 2, (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.configure(bg=self.ACCENT)

        self._drag_start = None
        self._resize_dir = None
        self._build_ui()
        self._bind_events()

    # ── build ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        B = self.BORDER

        self.inner = tk.Frame(self.root, bg=self.BG)
        self.inner.place(x=B, y=B, relwidth=1.0, relheight=1.0,
                         width=-2*B, height=-2*B)
        
        self.status_lbl = tk.Label(
            self.inner,
            text=self._size_text(),
            font=("Helvetica", 9),
            fg="#5599bb",
            bg=self.BG,
        )
        self.status_lbl.place(relx=0.5, rely=1.0, anchor="s", y=-6)
        
        # Resize handles
        self._handles = {}
        cursors = {
            "nw": "size_nw_se", "n": "size_ns",  "ne": "size_ne_sw",
            "w":  "size_we",                       "e":  "size_we",
            "sw": "size_ne_sw", "s": "size_ns",  "se": "size_nw_se",
        }
        for name, cur in cursors.items():
            f = tk.Frame(self.root, bg=self.ACCENT, cursor=cur)
            self._handles[name] = f
            f.bind("<ButtonPress-1>",   lambda e, d=name: self._start_resize(e, d))
            f.bind("<B1-Motion>",       self._do_resize)
            f.bind("<ButtonRelease-1>", self._stop_drag)

        self._place_handles()

    def _place_handles(self):
        H = self.HANDLE
        w = self.root.winfo_width()  or 520
        h = self.root.winfo_height() or 360
        specs = {
            "nw": (0,    0,    H,     H),
            "n":  (H,    0,    w-2*H, H),
            "ne": (w-H,  0,    H,     H),
            "w":  (0,    H,    H,     h-2*H),
            "e":  (w-H,  H,    H,     h-2*H),
            "sw": (0,    h-H,  H,     H),
            "s":  (H,    h-H,  w-2*H, H),
            "se": (w-H,  h-H,  H,     H),
        }
        for name, (x, y, fw, fh) in specs.items():
            self._handles[name].place(x=x, y=y, width=fw, height=fh)

    # ── events ───────────────────────────────────────────────────────────────
    def _bind_events(self):
        for widget in (self.inner, self.status_lbl):
            widget.bind("<ButtonPress-1>",   self._start_move)
            widget.bind("<B1-Motion>",       self._do_move)
            widget.bind("<ButtonRelease-1>", self._stop_drag)
        self.root.bind("<Configure>", self._on_configure)

    def _start_move(self, event):
        self._resize_dir = None
        self._drag_start = (event.x_root, event.y_root,
                            self.root.winfo_x(), self.root.winfo_y())

    def _do_move(self, event):
        if not self._drag_start:
            return
        ox, oy, wx, wy = self._drag_start
        self.root.geometry(f"+{wx + event.x_root - ox}+{wy + event.y_root - oy}")

    def _start_resize(self, event, direction):
        self._resize_dir = direction
        self._drag_start = (event.x_root, event.y_root,
                            self.root.winfo_x(), self.root.winfo_y(),
                            self.root.winfo_width(), self.root.winfo_height())

    def _do_resize(self, event):
        if not self._drag_start or not self._resize_dir:
            return
        ox, oy, wx, wy, ww, wh = self._drag_start
        dx, dy = event.x_root - ox, event.y_root - oy
        d  = self._resize_dir
        nx, ny, nw, nh = wx, wy, ww, wh
        if "e" in d: nw = max(self.MIN_SIZE, ww + dx)
        if "s" in d: nh = max(self.MIN_SIZE, wh + dy)
        if "w" in d: nw = max(self.MIN_SIZE, ww - dx); nx = wx + ww - nw
        if "n" in d: nh = max(self.MIN_SIZE, wh - dy); ny = wy + wh - nh
        self.root.geometry(f"{nw}x{nh}+{nx}+{ny}")

    def _stop_drag(self, _event):
        self._drag_start = None

    def _on_configure(self, _event):
        self._place_handles()
        self.status_lbl.configure(text=self._size_text())

    # ── helpers ──────────────────────────────────────────────────────────────
    def _size_text(self):
        try:
            B  = self.BORDER
            w  = self.root.winfo_width()
            h  = self.root.winfo_height()
            x  = self.root.winfo_x()
            y  = self.root.winfo_y()
            return f"Region: {w-2*B} × {h-2*B} px  |  pos ({x+B}, {y+B})"
        except Exception:
            return ""

    def get_region(self):
        """
        Returns capture box coordinates, scaled to device pixel ratio.
        """
        B = self.BORDER
        s = self.scale

        lx = self.root.winfo_x() + B
        ly = self.root.winfo_y() + B
        lw = self.root.winfo_width()  - 2 * B
        lh = self.root.winfo_height() - 2 * B

        # Convert logical → physical (round to nearest int)
        px1 = round(lx * s)
        py1 = round(ly * s)
        px2 = round((lx + lw) * s)
        py2 = round((ly + lh) * s)

        return (px1, py1, px2, py2)