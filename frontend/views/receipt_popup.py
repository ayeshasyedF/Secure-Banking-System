import tkinter as tk
import time
from frontend.theme import (
    BG_PRIMARY, CARD_BG, BORDER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, ACCENT, GREEN, RED, GOLD,
    SMALL_FONT
)


class ReceiptPopup:
    """
    Modal receipt popup shown after a transaction.

    Usage:
        ReceiptPopup(parent_root, action="DEPOSIT", amount=100.00, success=True, server_reply="...")
    """

    def __init__(self, parent, action, amount, success, server_reply=""):
        self.top = tk.Toplevel(parent)
        self.top.title("Transaction Receipt")
        self.top.geometry("380x360")
        self.top.configure(bg=BG_PRIMARY)
        self.top.resizable(False, False)
        self.top.grab_set()  # Modal

        # Center over parent
        parent.update_idletasks()
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw // 2) - 190
        y = py + (ph // 2) - 180
        self.top.geometry(f"380x360+{x}+{y}")

        self._build(action, amount, success, server_reply)

    def _build(self, action, amount, success, server_reply):
        status_color = GREEN if success else RED
        status_text = "APPROVED" if success else "DECLINED"
        icon = "✓" if success else "✕"

        # Card
        outer = tk.Frame(self.top, bg=BORDER, padx=1, pady=1)
        outer.pack(fill="both", expand=True, padx=16, pady=16)
        card = tk.Frame(outer, bg=CARD_BG)
        card.pack(fill="both", expand=True)

        # Top accent bar
        tk.Frame(card, bg=status_color, height=4).pack(fill="x")

        # Status badge
        badge_frame = tk.Frame(card, bg=CARD_BG)
        badge_frame.pack(pady=(20, 8))

        tk.Label(
            badge_frame,
            text=icon,
            font=("Courier New", 28, "bold"),
            fg=status_color,
            bg=CARD_BG
        ).pack()

        tk.Label(
            badge_frame,
            text=status_text,
            font=("Courier New", 16, "bold"),
            fg=status_color,
            bg=CARD_BG
        ).pack()

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=24, pady=12)

        # Receipt details
        rows = [
            ("ACTION", action.upper()),
            ("AMOUNT", f"${float(amount):,.2f} CAD"),
            ("STATUS", status_text),
            ("TIME", time.strftime("%Y-%m-%d  %H:%M:%S")),
        ]
        if server_reply:
            rows.append(("SERVER", server_reply[:36] + ("..." if len(server_reply) > 36 else "")))

        detail_frame = tk.Frame(card, bg=CARD_BG)
        detail_frame.pack(fill="x", padx=28)

        for label, value in rows:
            row = tk.Frame(detail_frame, bg=CARD_BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Courier New", 10, "bold"), fg=TEXT_PRIMARY if label != "AMOUNT" else status_color, bg=CARD_BG, anchor="w").pack(side="left")

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=24, pady=12)

        # Close button
        tk.Button(
            card,
            text="CLOSE",
            font=("Courier New", 10, "bold"),
            bg=BORDER,
            fg=TEXT_SECONDARY,
            activebackground=ACCENT,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=8,
            command=self.top.destroy
        ).pack(pady=(0, 20))