import tkinter as tk
from frontend.theme import (
    BG_PRIMARY, BG_SECONDARY, CARD_BG,
    TEXT_PRIMARY, TEXT_SECONDARY,
    HEADING_FONT, CARD_TITLE_FONT, BODY_FONT,
    create_screen_frame, create_card,
    create_primary_button, create_secondary_button, create_danger_button
)


class DashboardView:
    def __init__(self, app):
        self.app = app

    def build(self):
        screen = create_screen_frame(self.app.root)

        # Top bar
        top_bar = tk.Frame(screen, bg=BG_SECONDARY, height=70)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        tk.Label(
            top_bar,
            text=f"Welcome, {self.app.client.username}",
            font=HEADING_FONT,
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY
        ).pack(side="left", padx=30, pady=20)

        logout_button = create_danger_button(top_bar, "Logout", self.app.handle_logout)
        logout_button.pack(side="right", padx=30, pady=15, ipadx=12, ipady=6)

        # Main content
        content = tk.Frame(screen, bg=BG_PRIMARY)
        content.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            content,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_PRIMARY
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            content,
            text="Choose an action to continue.",
            font=BODY_FONT,
            fg=TEXT_SECONDARY,
            bg=BG_PRIMARY
        ).pack(anchor="w", pady=(0, 25))

        cards_row = tk.Frame(content, bg=BG_PRIMARY)
        cards_row.pack()

        # Deposit card
        deposit_card = create_card(cards_row, width=220, height=180)
        deposit_card.grid(row=0, column=0, padx=12)

        tk.Label(
            deposit_card,
            text="Deposit",
            font=CARD_TITLE_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG
        ).pack(pady=(28, 10))

        tk.Label(
            deposit_card,
            text="Add money securely to your account.",
            font=("Arial", 10),
            fg=TEXT_SECONDARY,
            bg=CARD_BG,
            wraplength=160,
            justify="center"
        ).pack(pady=(0, 18))

        deposit_button = create_primary_button(deposit_card, "Open", self.app.show_deposit_screen)
        deposit_button.pack(ipadx=20, ipady=6)

        # Balance placeholder
        balance_card = create_card(cards_row, width=220, height=180)
        balance_card.grid(row=0, column=1, padx=12)

        tk.Label(
            balance_card,
            text="Balance",
            font=CARD_TITLE_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG
        ).pack(pady=(28, 10))

        tk.Label(
            balance_card,
            text="Check your current account balance.",
            font=("Arial", 10),
            fg=TEXT_SECONDARY,
            bg=CARD_BG,
            wraplength=160,
            justify="center"
        ).pack(pady=(0, 18))

        create_secondary_button(balance_card, "Coming Soon", state="disabled").pack(ipadx=12, ipady=6)

        # Transactions placeholder
        transaction_card = create_card(cards_row, width=220, height=180)
        transaction_card.grid(row=0, column=2, padx=12)

        tk.Label(
            transaction_card,
            text="Transactions",
            font=CARD_TITLE_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG
        ).pack(pady=(28, 10))

        tk.Label(
            transaction_card,
            text="View transaction-related actions and history.",
            font=("Arial", 10),
            fg=TEXT_SECONDARY,
            bg=CARD_BG,
            wraplength=160,
            justify="center"
        ).pack(pady=(0, 18))

        create_secondary_button(transaction_card, "Coming Soon", state="disabled").pack(ipadx=12, ipady=6)

        return screen