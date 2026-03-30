import tkinter as tk
from frontend.theme import (
    BG_PRIMARY, BG_SECONDARY, CARD_BG, BORDER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, ACCENT, GREEN,
    SMALL_FONT,
    create_screen_frame, create_card, create_entry,
    create_success_button, create_divider
)


class DepositView:
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
            text="DEPOSIT FUNDS",
            font=("Courier New", 12, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY
        ).pack(side="left", padx=8, pady=20)

        tk.Frame(screen, bg=BORDER, height=1).pack(fill="x")

        content = tk.Frame(screen, bg=BG_PRIMARY)
        content.pack(fill="both", expand=True)

        wrapper = tk.Frame(content, bg=BG_PRIMARY)
        wrapper.pack(side="top", fill="both", expand=True)

        outer_card, card = create_card(wrapper, width=440, height=360)
        outer_card.pack(anchor="center", expand=True)

        tk.Frame(card, bg=GREEN, height=3).pack(fill="x")

        header_frame = tk.Frame(card, bg=CARD_BG)
        header_frame.pack(fill="x", padx=32, pady=(20, 0))

        tk.Label(header_frame, text="▲", font=("Courier New", 20), fg=GREEN, bg=CARD_BG).pack(side="left", padx=(0, 12))

        title_stack = tk.Frame(header_frame, bg=CARD_BG)
        title_stack.pack(side="left")
        tk.Label(title_stack, text="MAKE A DEPOSIT", font=("Courier New", 14, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG, anchor="w").pack(anchor="w")
        tk.Label(title_stack, text="Funds are credited instantly", font=("Courier New", 9), fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(anchor="w")

        create_divider(card, pady=16)

        # All form elements in one frame, in order
        form = tk.Frame(card, bg=CARD_BG)
        form.pack(fill="x", padx=32)

        tk.Label(form, text="AMOUNT  (CAD)", font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x")

        amount_row = tk.Frame(form, bg=CARD_BG)
        amount_row.pack(fill="x", pady=(6, 16))
        tk.Label(amount_row, text="$", font=("Courier New", 18, "bold"), fg=GREEN, bg=CARD_BG).pack(side="left", padx=(0, 6))

        self.app.deposit_entry_frame = create_entry(amount_row)
        self.app.deposit_entry = self.app.deposit_entry_frame.entry_widget
        self.app.deposit_entry.config(font=("Courier New", 18, "bold"), width=16, fg=TEXT_PRIMARY)
        self.app.deposit_entry_frame.pack(side="left", fill="x", expand=True)

        tk.Label(form, text="QUICK SELECT", font=("Courier New", 8), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")

        btns_frame = tk.Frame(form, bg=CARD_BG)
        btns_frame.pack(fill="x", pady=(6, 20))
        for amount in [50, 100, 250, 500]:
            tk.Button(
                btns_frame, text=f"${amount}", font=("Courier New", 9, "bold"),
                bg=BORDER, fg=TEXT_SECONDARY, activebackground=GREEN, activeforeground="#ffffff",
                relief="flat", cursor="hand2", padx=10, pady=5,
                command=lambda a=amount: self._quick_fill(a)
            ).pack(side="left", padx=(0, 8))

        create_success_button(card, "CONFIRM DEPOSIT  →", self.app.handle_deposit).pack(padx=32, fill="x", ipady=4)

        self.app.deposit_result_label = tk.Label(
            card, text="", font=("Courier New", 9), fg=ACCENT, bg=CARD_BG, wraplength=360, justify="center"
        )
        self.app.deposit_result_label.pack(pady=(10, 4))

        return screen

    def _quick_fill(self, amount):
        self.app.deposit_entry.delete(0, tk.END)
        self.app.deposit_entry.insert(0, str(amount))