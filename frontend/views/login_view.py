import tkinter as tk
from frontend.theme import (
    BG_PRIMARY, CARD_BG, TEXT_PRIMARY, TEXT_SECONDARY,
    TITLE_FONT, SUBTITLE_FONT, LABEL_FONT,
    create_screen_frame, create_card, create_entry,
    create_primary_button, create_secondary_button
)


class LoginView:
    def __init__(self, app):
        self.app = app

    def build(self):
        screen = create_screen_frame(self.app.root)

        wrapper = tk.Frame(screen, bg=BG_PRIMARY)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        card = create_card(wrapper, width=420, height=380)
        card.pack()

        tk.Label(
            card,
            text="Secure Banking ATM",
            font=TITLE_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG
        ).pack(pady=(30, 10))

        tk.Label(
            card,
            text="Login to continue",
            font=SUBTITLE_FONT,
            fg=TEXT_SECONDARY,
            bg=CARD_BG
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="Username",
            font=LABEL_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            anchor="w"
        ).pack(fill="x", padx=40)

        self.app.username_entry = create_entry(card)
        self.app.username_entry.pack(padx=40, pady=(6, 18))

        tk.Label(
            card,
            text="Password",
            font=LABEL_FONT,
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            anchor="w"
        ).pack(fill="x", padx=40)

        self.app.password_entry = create_entry(card, show="*")
        self.app.password_entry.pack(padx=40, pady=(6, 24))

        login_button = create_primary_button(card, "Login", self.app.handle_login)
        login_button.pack(pady=(0, 15), ipadx=80)

        register_button = create_secondary_button(
            card,
            "Register (Coming Soon)",
            state="disabled"
        )
        register_button.pack()
        
        return screen