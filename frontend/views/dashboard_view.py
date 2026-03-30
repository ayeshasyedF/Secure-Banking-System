import tkinter as tk
import time
from frontend.theme import (
    BG_PRIMARY, BG_SECONDARY, CARD_BG, BORDER, BORDER_LIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, ACCENT, ACCENT_BG, GOLD,
    GREEN, RED,
    HEADING_FONT, CARD_TITLE_FONT, BODY_FONT, SMALL_FONT,
    create_screen_frame, create_card,
    create_primary_button, create_secondary_button,
    create_danger_button, create_divider
)


class DashboardView:
    def __init__(self, app):
        self.app = app

    def build(self):
        screen = create_screen_frame(self.app.root)

        # Sidebar
        sidebar = tk.Frame(screen, bg="#080d14", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Sidebar right border
        tk.Frame(screen, bg=BORDER, width=1).pack(side="left", fill="y")

        # Sidebar header
        tk.Label(
            sidebar,
            text="◈  VAULT",
            font=("Courier New", 14, "bold"),
            fg=ACCENT,
            bg="#080d14"
        ).pack(pady=(28, 4), padx=24, anchor="w")

        tk.Label(
            sidebar,
            text="SECURE BANKING",
            font=("Courier New", 8),
            fg=TEXT_MUTED,
            bg="#080d14"
        ).pack(padx=24, anchor="w")

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=24, pady=20)

        # Nav items
        nav_items = [
            ("▣  Dashboard", True),
            ("⬛  Deposit", False),
            ("◻  Balance", False),
            ("≡  Transactions", True),  # Changed to True
        ]

        for label, active in nav_items:
            is_deposit = "Deposit" in label
            is_balance = "Balance" in label
            is_transactions = "Transactions" in label

            bg = ACCENT_BG if active else "#080d14"
            fg = ACCENT if active else TEXT_MUTED

            cmd = None
            if is_deposit:
                cmd = self.app.show_deposit_screen
            elif is_balance:
                cmd = self.app.show_balance_screen
            elif is_transactions:
                cmd = self.app.show_transactions_screen  # Added this

            btn = tk.Button(
                sidebar,
                text=label,
                font=("Courier New", 10, "bold") if active else ("Courier New", 10),
                fg=fg,
                bg=bg,
                activebackground=CARD_BG,
                activeforeground=TEXT_PRIMARY,
                relief="flat",
                anchor="w",
                padx=24,
                pady=10,
                cursor="hand2" if cmd else "arrow",
                command=cmd,
                state="normal" if cmd or active else "disabled"
            )
            btn.pack(fill="x")

            if is_transactions and not active:  # Remove the "COMING SOON" since it's now active
                tk.Label(
                    sidebar,
                    text="COMING SOON",
                    font=("Courier New", 7, "bold"),
                    fg=ACCENT,
                    bg="#080d14"
                ).pack(padx=48, anchor="w", pady=(0, 4))

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=24, pady=16)

        # User info at bottom of sidebar
        user_frame = tk.Frame(sidebar, bg="#080d14")
        user_frame.pack(side="bottom", fill="x", padx=24, pady=24)

        tk.Label(
            user_frame,
            text="LOGGED IN AS",
            font=("Courier New", 8),
            fg=TEXT_MUTED,
            bg="#080d14"
        ).pack(anchor="w")

        tk.Label(
            user_frame,
            text=self.app.client.username.upper(),
            font=("Courier New", 11, "bold"),
            fg=TEXT_PRIMARY,
            bg="#080d14"
        ).pack(anchor="w", pady=(2, 12))

        logout_btn = create_danger_button(user_frame, "SIGN OUT", self.app.handle_logout)
        logout_btn.pack(fill="x", ipady=4)

        # Main content
        main = tk.Frame(screen, bg=BG_PRIMARY)
        main.pack(side="left", fill="both", expand=True)

        # Top bar
        topbar = tk.Frame(main, bg=BG_SECONDARY, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(
            topbar,
            text="DASHBOARD",
            font=("Courier New", 12, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY
        ).pack(side="left", padx=32, pady=20)

        # Timestamp
        ts = time.strftime("%Y-%m-%d  %H:%M")
        tk.Label(
            topbar,
            text=ts,
            font=("Courier New", 9),
            fg=TEXT_MUTED,
            bg=BG_SECONDARY
        ).pack(side="right", padx=32, pady=20)

        tk.Frame(main, bg=BORDER, height=1).pack(fill="x")

        # Content area
        content = tk.Frame(main, bg=BG_PRIMARY)
        content.pack(fill="both", expand=True, padx=36, pady=28)

        tk.Label(
            content,
            text=f"Good to see you, {self.app.client.username.upper()}.",
            font=("Courier New", 20, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_PRIMARY
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Select a service to get started.",
            font=("Courier New", 10),
            fg=TEXT_MUTED,
            bg=BG_PRIMARY
        ).pack(anchor="w", pady=(4, 24))

        tk.Frame(content, bg=BORDER, height=1).pack(fill="x", pady=(0, 24))

        # Cards row
        cards_row = tk.Frame(content, bg=BG_PRIMARY)
        cards_row.pack(anchor="w")
        cards_row.pack_propagate(False)

        self._make_action_card(
            cards_row,
            icon="▲",
            title="DEPOSIT",
            desc="Add funds securely to your account with instant processing.",
            btn_text="OPEN  →",
            btn_cmd=self.app.show_deposit_screen,
            btn_color=GREEN,
            btn_hover="#34d399",
            active=True
        )

        self._make_action_card(
            cards_row,
            icon="◉",
            title="BALANCE",
            desc="View your current account balance and available funds.",
            btn_text="VIEW  →",
            btn_cmd=self.app.show_balance_screen,
            btn_color=ACCENT,
            btn_hover="#38bdf8",
            active=True
        )

        self._make_action_card(
            cards_row, col=2,
            icon="≡",
            title="TRANSACTIONS",
            desc="View your full transaction history and activity logs.",
            btn_text="VIEW HISTORY →",
            btn_cmd=self.app.show_transactions_screen,
            btn_color="#1e3a5f",
            btn_hover="#2a4a70",
            active=True
        )

        # Security notice
        notice = tk.Frame(content, bg="#0a1628", pady=12)
        notice.pack(fill="x", pady=(32, 0))
        tk.Frame(notice, bg=ACCENT, width=3).pack(side="left", fill="y", padx=(16, 12))
        tk.Label(
            notice,
            text="▸  This session is encrypted with AES-256. All transactions are monitored and logged securely.",
            font=("Courier New", 9),
            fg=TEXT_MUTED,
            bg="#0a1628"
        ).pack(side="left")

        return screen

    def _make_action_card(self, parent, icon, title, desc, btn_text, btn_cmd, btn_color, btn_hover, active, col=None):
        outer, card = create_card(parent, width=196, height=220)
        outer.pack(side="left", padx=10)

        icon_frame = tk.Frame(card, bg=CARD_BG)
        icon_frame.pack(pady=(24, 8))

        tk.Label(
            icon_frame,
            text=icon,
            font=("Courier New", 24),
            fg=btn_color if active else TEXT_MUTED,
            bg=CARD_BG
        ).pack()

        tk.Label(
            card,
            text=title,
            font=("Courier New", 12, "bold"),
            fg=TEXT_PRIMARY if active else TEXT_MUTED,
            bg=CARD_BG
        ).pack()

        tk.Label(
            card,
            text=desc,
            font=("Courier New", 8),
            fg=TEXT_MUTED,
            bg=CARD_BG,
            wraplength=160,
            justify="center"
        ).pack(pady=(6, 14))

        btn = tk.Button(
            card,
            text=btn_text,
            font=("Courier New", 9, "bold"),
            bg=btn_color,
            fg="#ffffff" if active else TEXT_MUTED,
            activebackground=btn_hover,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2" if active else "arrow",
            command=btn_cmd,
            state="normal" if active else "disabled",
            padx=16,
            pady=6
        )
        btn.pack()