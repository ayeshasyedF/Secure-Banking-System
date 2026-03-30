import tkinter as tk
import time
from frontend.theme import (
    BG_PRIMARY, BG_SECONDARY, CARD_BG, BORDER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, ACCENT, GREEN, GOLD,
    SMALL_FONT,
    create_screen_frame, create_card, create_divider
)


class BalanceView:
    def __init__(self, app):
        self.app = app

    def build(self):
        screen = create_screen_frame(self.app.root)

        # Top bar
        topbar = tk.Frame(screen, bg=BG_SECONDARY, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        back_btn = tk.Button(
            topbar,
            text="←  DASHBOARD",
            font=("Courier New", 10, "bold"),
            bg=BG_SECONDARY,
            fg=TEXT_MUTED,
            activebackground=BG_SECONDARY,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            command=self.app.show_dashboard
        )
        back_btn.pack(side="left", padx=28, pady=20)

        tk.Label(
            topbar,
            text="ACCOUNT BALANCE",
            font=("Courier New", 12, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY
        ).pack(side="left", padx=8, pady=20)

        tk.Frame(screen, bg=BORDER, height=1).pack(fill="x")

        content = tk.Frame(screen, bg=BG_PRIMARY)
        content.pack(fill="both", expand=True)

        wrapper = tk.Frame(content, bg=BG_PRIMARY)
        wrapper.pack(side="top", fill="both", expand=True)

        outer_card, card = create_card(wrapper, width=460, height=340)
        outer_card.pack(anchor="center", expand=True)

        tk.Frame(card, bg=ACCENT, height=3).pack(fill="x")

        # Header
        header = tk.Frame(card, bg=CARD_BG)
        header.pack(fill="x", padx=32, pady=(20, 0))

        tk.Label(
            header,
            text="◉",
            font=("Courier New", 20),
            fg=ACCENT,
            bg=CARD_BG
        ).pack(side="left", padx=(0, 12))

        title_stack = tk.Frame(header, bg=CARD_BG)
        title_stack.pack(side="left")

        tk.Label(
            title_stack,
            text="CURRENT BALANCE",
            font=("Courier New", 14, "bold"),
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            anchor="w"
        ).pack(anchor="w")

        tk.Label(
            title_stack,
            text=f"Account: {self.app.client.username.upper()}",
            font=("Courier New", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG,
            anchor="w"
        ).pack(anchor="w")

        create_divider(card, pady=16)

        # Balance display
        balance_frame = tk.Frame(card, bg=CARD_BG)
        balance_frame.pack(pady=(0, 8))

        self.app.balance_display = tk.Label(
            balance_frame,
            text="$ -.--",
            font=("Courier New", 38, "bold"),
            fg=TEXT_MUTED,
            bg=CARD_BG
        )
        self.app.balance_display.pack()

        tk.Label(
            balance_frame,
            text="CANADIAN DOLLARS",
            font=("Courier New", 8),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack()

        create_divider(card, pady=12)

        # Footer row
        footer = tk.Frame(card, bg=CARD_BG)
        footer.pack(fill="x", padx=32, pady=(0, 20))

        # Last updated
        self.app.balance_timestamp = tk.Label(
            footer,
            text="Not yet fetched",
            font=("Courier New", 8),
            fg=TEXT_MUTED,
            bg=CARD_BG
        )
        self.app.balance_timestamp.pack(side="left")

        # Refresh button
        self.app.balance_status_label = tk.Label(
            footer,
            text="",
            font=("Courier New", 9),
            fg=ACCENT,
            bg=CARD_BG
        )
        self.app.balance_status_label.pack(side="left", padx=12)

        refresh_btn = tk.Button(
            footer,
            text="⟳  REFRESH",
            font=("Courier New", 10, "bold"),
            bg=ACCENT,
            fg="#ffffff",
            activebackground="#38bdf8",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            command=self.app.handle_balance_refresh
        )
        refresh_btn.pack(side="right")

        # Auto-fetch on load
        screen.after(200, self.app.handle_balance_refresh)

        return screen