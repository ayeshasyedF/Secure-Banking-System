import tkinter as tk
from frontend.theme import (
    BG_PRIMARY, BG_SECONDARY, CARD_BG,
    TEXT_PRIMARY, TEXT_SECONDARY, INFO,
    HEADING_FONT, TITLE_FONT, SUBTITLE_FONT, LABEL_FONT,
    create_screen_frame, create_card, create_entry,
    create_success_button, create_secondary_button
)


class DepositView:
    def __init__(self, app):
        self.app = app

    def build(self):
        screen = create_screen_frame(self.app.root)

        top_bar = tk.Frame(screen, bg=BG_SECONDARY, height=70)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        tk.Label(
            top_bar,
            text="Deposit Funds",
            font=HEADING_FONT,
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY
        ).pack(side="left", padx=30, pady=20)

        back_button = create_secondary_button(top_bar, "Back", self.app.show_dashboard)
        back_button.pack(side="right", padx=30, pady=15, ipadx=12, ipady=6)

        content = tk.Frame(screen, bg=BG_PRIMARY)
        content.pack(fill="both", expand=True)

        wrapper = tk.Frame(content, bg=BG_PRIMARY)
        wrapper.place(relx=0.5, rely=0.45, anchor="center")

        card = create_card(wrapper, width=430, height=320)
        card.pack()

        tk.Label(
            card,
            text="Make a Deposit",
            font=TITLE_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG
        ).pack(pady=(30, 10))

        tk.Label(
            card,
            text="Enter the amount you would like to deposit.",
            font=SUBTITLE_FONT,
            fg=TEXT_SECONDARY,
            bg=CARD_BG
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="Amount",
            font=LABEL_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            anchor="w"
        ).pack(fill="x", padx=40)

        self.app.deposit_entry = create_entry(card)
        self.app.deposit_entry.pack(padx=40, pady=(6, 20))

        submit_button = create_success_button(card, "Submit Deposit", self.app.handle_deposit)
        submit_button.pack(pady=(0, 18), ipadx=50)

        self.app.deposit_result_label = tk.Label(
            card,
            text="",
            font=("Arial", 11),
            fg=INFO,
            bg=CARD_BG,
            wraplength=320,
            justify="center"
        )
        self.app.deposit_result_label.pack()

        return screen