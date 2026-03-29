import tkinter as tk

# -----------------------------
# COLORS
# -----------------------------
BG_PRIMARY = "#0f172a"       # main dark background
BG_SECONDARY = "#111827"     # top bar background
CARD_BG = "#1e293b"          # card background
BORDER = "#334155"

TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#cbd5e1"

BLUE = "#3b82f6"
BLUE_HOVER = "#2563eb"

GREEN = "#22c55e"
GREEN_HOVER = "#16a34a"

RED = "#ef4444"
RED_HOVER = "#dc2626"

GRAY = "#334155"
GRAY_HOVER = "#475569"

SUCCESS = "#86efac"
ERROR = "#fca5a5"
INFO = "#93c5fd"

# -----------------------------
# FONTS
# -----------------------------
TITLE_FONT = ("Arial", 22, "bold")
SUBTITLE_FONT = ("Arial", 11)
HEADING_FONT = ("Arial", 18, "bold")
CARD_TITLE_FONT = ("Arial", 16, "bold")
LABEL_FONT = ("Arial", 11, "bold")
BODY_FONT = ("Arial", 11)
BUTTON_FONT = ("Arial", 12, "bold")
SMALL_BUTTON_FONT = ("Arial", 10)

# -----------------------------
# REUSABLE UI HELPERS
# -----------------------------
def create_screen_frame(root):
    frame = tk.Frame(root, bg=BG_PRIMARY)
    frame.pack(fill="both", expand=True)
    return frame


def create_card(parent, width=420, height=360):
    card = tk.Frame(
        parent,
        bg=CARD_BG,
        width=width,
        height=height,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    card.pack_propagate(False)
    return card


def create_primary_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        font=BUTTON_FONT,
        bg=BLUE,
        fg=TEXT_PRIMARY,
        activebackground=BLUE_HOVER,
        activeforeground=TEXT_PRIMARY,
        relief="flat",
        padx=12,
        pady=10,
        command=command
    )


def create_success_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        font=BUTTON_FONT,
        bg=GREEN,
        fg=TEXT_PRIMARY,
        activebackground=GREEN_HOVER,
        activeforeground=TEXT_PRIMARY,
        relief="flat",
        padx=12,
        pady=10,
        command=command
    )


def create_danger_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        font=("Arial", 11, "bold"),
        bg=RED,
        fg=TEXT_PRIMARY,
        activebackground=RED_HOVER,
        activeforeground=TEXT_PRIMARY,
        relief="flat",
        command=command
    )


def create_secondary_button(parent, text, command=None, state="normal"):
    return tk.Button(
        parent,
        text=text,
        font=("Arial", 11, "bold"),
        bg=GRAY,
        fg=TEXT_SECONDARY if state == "disabled" else TEXT_PRIMARY,
        activebackground=GRAY_HOVER,
        activeforeground=TEXT_PRIMARY,
        relief="flat",
        command=command,
        state=state
    )


def create_entry(parent, show=None, width=28):
    return tk.Entry(
        parent,
        font=("Arial", 12),
        width=width,
        relief="flat",
        bd=8,
        show=show
    )