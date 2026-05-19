import tkinter as tk
from frontend.theme import (
    BG_PRIMARY, CARD_BG, BORDER, BORDER_LIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, ACCENT,
    SMALL_FONT, BUTTON_FONT,
    create_screen_frame, create_card, create_entry,
    create_primary_button, create_secondary_button, create_divider
)


class RegisterView:
    def __init__(self, app):
        self.app = app

    def build(self):
        screen = create_screen_frame(self.app.root)

        # Subtle bg pattern
        canvas = tk.Canvas(screen, bg=BG_PRIMARY, highlightthickness=0)
        canvas.place(relwidth=1, relheight=1)
        for x in range(0, 900, 40):
            canvas.create_line(x, 0, x, 600, fill="#0d1a2a", width=1)
        for y in range(0, 600, 40):
            canvas.create_line(0, y, 900, y, fill="#0d1a2a", width=1)

        wrapper = tk.Frame(screen, bg=BG_PRIMARY)
        wrapper.pack(side="top", fill="both", expand=True)

        outer_card, card = create_card(wrapper, width=420, height=480)
        outer_card.pack(anchor="center", expand=True)

        # Accent top bar
        tk.Frame(card, bg=ACCENT, height=3).pack(fill="x")

        # Header
        header = tk.Frame(card, bg=CARD_BG)
        header.pack(fill="x", padx=32, pady=(20, 0))

        tk.Label(
            header,
            text="◈  VAULT",
            font=("Courier New", 13, "bold"),
            fg=ACCENT,
            bg=CARD_BG
        ).pack(side="left")

        tk.Label(
            card,
            text="CREATE ACCOUNT",
            font=("Courier New", 18, "bold"),
            fg=TEXT_PRIMARY,
            bg=CARD_BG
        ).pack(pady=(12, 4))

        tk.Label(
            card,
            text="Set up your secure banking profile",
            font=SMALL_FONT,
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(pady=(0, 16))

        create_divider(card)

        form = tk.Frame(card, bg=CARD_BG)
        form.pack(fill="x", padx=32, pady=(16, 0))

        tk.Label(form, text="USERNAME", font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x")
        self._user_frame = create_entry(form)
        self.app.register_username_entry = self._user_frame.entry_widget
        self._user_frame.pack(pady=(4, 14), fill="x")

        tk.Label(form, text="PASSWORD", font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x")
        self._pass_frame = create_entry(form, show="●")
        self.app.register_password_entry = self._pass_frame.entry_widget
        self._pass_frame.pack(pady=(4, 14), fill="x")

        tk.Label(form, text="CONFIRM PASSWORD", font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x")
        self._confirm_frame = create_entry(form, show="●")
        self.app.register_confirm_entry = self._confirm_frame.entry_widget
        self._confirm_frame.pack(pady=(4, 16), fill="x")

        register_btn = create_primary_button(card, "CREATE ACCOUNT  →", self.app.handle_register)
        register_btn.pack(padx=32, fill="x", ipady=4)

        back_btn = tk.Button(
            card,
            text="← BACK TO SIGN IN",
            font=("Courier New", 9, "bold"),
            bg=CARD_BG,
            fg=TEXT_MUTED,
            activebackground=CARD_BG,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            command=self.app.show_login_screen
        )
        back_btn.pack(pady=(10, 4))

        self.app.register_result_label = tk.Label(
            card, text="", font=SMALL_FONT, fg="#ef4444", bg=CARD_BG, wraplength=340
        )
        self.app.register_result_label.pack(pady=(0, 8))

        return screen
