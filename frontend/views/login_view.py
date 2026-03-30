import tkinter as tk
from frontend.theme import (
    BG_PRIMARY, BG_SECONDARY, CARD_BG, BORDER, BORDER_LIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, ACCENT, GOLD,
    TITLE_FONT, SUBTITLE_FONT, LABEL_FONT, SMALL_FONT, BUTTON_FONT,
    create_screen_frame, create_card, create_entry,
    create_primary_button, create_secondary_button, create_divider
)


class LoginView:
    def __init__(self, app):
        self.app = app
        self._username_frame = None
        self._password_frame = None

    def build(self):
        screen = create_screen_frame(self.app.root)

        # Background grid pattern
        canvas = tk.Canvas(screen, bg=BG_PRIMARY, highlightthickness=0)
        canvas.place(relwidth=1, relheight=1)
        self._draw_grid(canvas, screen)

        # Left branding panel
        left = tk.Frame(screen, bg="#080d14", width=340)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Frame(left, bg=ACCENT, width=3).pack(side="right", fill="y")

        branding = tk.Frame(left, bg="#080d14")
        branding.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            branding,
            text="◈",
            font=("Courier New", 48),
            fg=ACCENT,
            bg="#080d14"
        ).pack(pady=(0, 16))

        tk.Label(
            branding,
            text="V A U L T",
            font=("Courier New", 28, "bold"),
            fg=TEXT_PRIMARY,
            bg="#080d14"
        ).pack()

        tk.Label(
            branding,
            text="SECURE BANKING",
            font=("Courier New", 9),
            fg=TEXT_MUTED,
            bg="#080d14"
        ).pack(pady=(4, 0))

        tk.Frame(branding, bg=ACCENT, height=2, width=120).pack(pady=24)

        for line in ["256-bit encryption", "Real-time monitoring", "Zero-trust architecture"]:
            row = tk.Frame(branding, bg="#080d14")
            row.pack(anchor="w", pady=3)
            tk.Label(row, text="▸", fg=ACCENT, bg="#080d14", font=("Courier New", 9)).pack(side="left", padx=(0, 8))
            tk.Label(row, text=line, fg=TEXT_SECONDARY, bg="#080d14", font=("Courier New", 9)).pack(side="left")

        # Right login panel
        right = tk.Frame(screen, bg=BG_PRIMARY)
        right.pack(side="left", fill="both", expand=True)

        wrapper = tk.Frame(right, bg=BG_PRIMARY)
        wrapper.pack(side="top", fill="both", expand=True)

        # Card
        outer_card, card = create_card(wrapper, width=380, height=400)
        outer_card.pack(anchor="center", expand=True)

        # Card header accent line
        tk.Frame(card, bg=ACCENT, height=3).pack(fill="x")

        tk.Label(
            card,
            text="SIGN IN",
            font=("Courier New", 18, "bold"),
            fg=TEXT_PRIMARY,
            bg=CARD_BG
        ).pack(pady=(24, 4))

        tk.Label(
            card,
            text="Enter your credentials to access your account",
            font=SMALL_FONT,
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(pady=(0, 20))

        create_divider(card, pady=0)

        # Single form frame — all labels AND entries go here in order
        form = tk.Frame(card, bg=CARD_BG)
        form.pack(fill="x", padx=32, pady=(20, 16))

        tk.Label(form, text="USERNAME", font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x")
        self._username_frame = create_entry(form)
        self.app.username_entry = self._username_frame.entry_widget
        self._username_frame.pack(pady=(4, 16), fill="x")

        tk.Label(form, text="PASSWORD", font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x")
        self._password_frame = create_entry(form, show="●")
        self.app.password_entry = self._password_frame.entry_widget
        self._password_frame.pack(pady=(4, 0), fill="x")

        # Bind enter key
        self.app.root.bind("<Return>", lambda e: self.app.handle_login())

        login_btn = create_primary_button(card, "ACCESS ACCOUNT  →", self.app.handle_login)
        login_btn.pack(padx=32, pady=(16, 10), fill="x", ipady=4)

        register_btn = tk.Button(
            card,
            text="CREATE NEW ACCOUNT",
            font=("Courier New", 9, "bold"),
            bg=CARD_BG,
            fg=ACCENT,
            activebackground=CARD_BG,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            command=self.app.show_register_screen
        )
        register_btn.pack(pady=(0, 8))

        # Status label
        self.app.login_error_label = tk.Label(
            card, text="", font=SMALL_FONT, fg="#ef4444", bg=CARD_BG, wraplength=300
        )
        self.app.login_error_label.pack(pady=(0, 8))

        return screen

    def _draw_grid(self, canvas, parent):
        parent.update_idletasks()
        w, h = 900, 600
        for x in range(0, w, 40):
            canvas.create_line(x, 0, x, h, fill="#0d1a2a", width=1)
        for y in range(0, h, 40):
            canvas.create_line(0, y, w, y, fill="#0d1a2a", width=1)