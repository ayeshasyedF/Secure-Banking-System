import tkinter as tk

# -----------------------------
# COLORS - Refined dark banking palette
# -----------------------------
BG_PRIMARY = "#080d14"       # Deep navy black
BG_SECONDARY = "#0d1520"     # Slightly lighter nav bg
CARD_BG = "#111c2d"          # Card surface
CARD_BG_HOVER = "#162236"
BORDER = "#1e3a5f"
BORDER_LIGHT = "#2a4a70"

TEXT_PRIMARY = "#e8f4ff"
TEXT_SECONDARY = "#7a9cc0"
TEXT_MUTED = "#3d5a7a"

ACCENT = "#0ea5e9"           # Sky blue accent
ACCENT_HOVER = "#38bdf8"
ACCENT_BG = "#0d2438"        # Subtle accent background
ACCENT_GLOW = "#0ea5e920"

BLUE = "#0ea5e9"
BLUE_HOVER = "#38bdf8"
BLUE_DARK = "#0369a1"

GREEN = "#10b981"
GREEN_HOVER = "#34d399"
GREEN_DARK = "#065f46"

RED = "#ef4444"
RED_HOVER = "#f87171"
RED_DARK = "#7f1d1d"

GRAY = "#1e3a5f"
GRAY_HOVER = "#2a4a70"

GOLD = "#f59e0b"

SUCCESS = "#6ee7b7"
SUCCESS_BG = "#064e3b"
ERROR = "#fca5a5"
ERROR_BG = "#450a0a"
INFO = "#7dd3fc"
INFO_BG = "#0c4a6e"
WARNING_BG = "#451a03"

# -----------------------------
# FONTS - Distinctive monospaced feel for banking
# -----------------------------
TITLE_FONT    = ("Courier New", 20, "bold")
SUBTITLE_FONT = ("Courier New", 10)
HEADING_FONT  = ("Courier New", 16, "bold")
CARD_TITLE_FONT = ("Courier New", 14, "bold")
LABEL_FONT    = ("Courier New", 10, "bold")
BODY_FONT     = ("Courier New", 10)
BUTTON_FONT   = ("Courier New", 11, "bold")
SMALL_FONT    = ("Courier New", 9)
MONO_LARGE    = ("Courier New", 28, "bold")
MONO_MEDIUM   = ("Courier New", 18, "bold")
BALANCE_FONT  = ("Courier New", 36, "bold")

# -----------------------------
# REUSABLE UI HELPERS
# -----------------------------
def create_screen_frame(root):
    frame = tk.Frame(root, bg=BG_PRIMARY)
    frame.pack(fill="both", expand=True)
    return frame


def create_card(parent, width=420, height=360):
    outer = tk.Frame(
        parent,
        bg=BORDER,
        highlightthickness=0,
    )
    card = tk.Frame(
        outer,
        bg=CARD_BG,
        width=width,
        height=height,
        highlightthickness=1,
        highlightbackground=BORDER,
    )
    card.pack_propagate(False)
    card.pack(padx=1, pady=1)
    return outer, card


def create_divider(parent, color=BORDER, pady=0):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", pady=pady)


def create_primary_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        font=BUTTON_FONT,
        bg=BLUE,
        fg="#ffffff",
        activebackground=BLUE_HOVER,
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        padx=16,
        pady=10,
        command=command
    )
    return btn


def create_success_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        font=BUTTON_FONT,
        bg=GREEN,
        fg="#ffffff",
        activebackground=GREEN_HOVER,
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        padx=16,
        pady=10,
        command=command
    )


def create_danger_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        font=("Courier New", 10, "bold"),
        bg=RED_DARK,
        fg=ERROR,
        activebackground=RED,
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=6,
        command=command
    )


def create_secondary_button(parent, text, command=None, state="normal"):
    return tk.Button(
        parent,
        text=text,
        font=("Courier New", 10, "bold"),
        bg=GRAY,
        fg=TEXT_MUTED if state == "disabled" else TEXT_SECONDARY,
        activebackground=GRAY_HOVER,
        activeforeground=TEXT_PRIMARY,
        relief="flat",
        cursor="hand2" if state == "normal" else "arrow",
        command=command,
        state=state
    )


def create_entry(parent, show=None, width=28):
    frame = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    entry = tk.Entry(
        frame,
        font=("Courier New", 12),
        width=width,
        relief="flat",
        bd=8,
        show=show,
        bg="#0a1628",
        fg=TEXT_PRIMARY,
        insertbackground=ACCENT,
        selectbackground=BLUE_DARK,
    )
    entry.pack()
    # Return the frame so it can be packed, but attach entry to frame
    frame.entry_widget = entry
    return frame


def create_label_tag(parent, text, color=ACCENT, bg=CARD_BG):
    """Small badge/tag label"""
    f = tk.Frame(parent, bg=color, padx=6, pady=2)
    tk.Label(f, text=text, font=SMALL_FONT, fg=BG_PRIMARY, bg=color).pack()
    return f