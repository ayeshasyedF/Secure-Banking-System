import tkinter as tk
from tkinter import ttk
from backend.audit import read_decrypted_logs
from frontend.theme import (
    BG_PRIMARY, BG_SECONDARY, CARD_BG, BORDER, BORDER_LIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, ACCENT, GOLD,
    SMALL_FONT,
    create_screen_frame, create_card, create_divider
)


class TransactionsView:
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
            text="TRANSACTION HISTORY",
            font=("Courier New", 12, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_SECONDARY
        ).pack(side="left", padx=8, pady=20)

        tk.Frame(screen, bg=BORDER, height=1).pack(fill="x")

        content = tk.Frame(screen, bg=BG_PRIMARY)
        content.pack(fill="both", expand=True)

        wrapper = tk.Frame(content, bg=BG_PRIMARY)
        wrapper.pack(side="top", fill="both", expand=True)

        outer_card, card = create_card(wrapper, width=700, height=500)
        outer_card.pack(anchor="center", expand=True)

        tk.Frame(card, bg=ACCENT, height=3).pack(fill="x")

        # Header
        header = tk.Frame(card, bg=CARD_BG)
        header.pack(fill="x", padx=32, pady=(20, 0))

        tk.Label(
            header,
            text="📋",
            font=("Courier New", 20),
            fg=ACCENT,
            bg=CARD_BG
        ).pack(side="left", padx=(0, 12))

        title_stack = tk.Frame(header, bg=CARD_BG)
        title_stack.pack(side="left")

        tk.Label(
            title_stack,
            text="TRANSACTION HISTORY",
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

        # Transactions list
        list_frame = tk.Frame(card, bg=CARD_BG)
        list_frame.pack(fill="both", expand=True, padx=32, pady=(0, 20))

        # Create treeview for transactions
        columns = ("timestamp", "action", "details")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        # Define headings
        tree.heading("timestamp", text="Date & Time")
        tree.heading("action", text="Action")
        tree.heading("details", text="Details")

        # Define column widths
        tree.column("timestamp", width=150, minwidth=150)
        tree.column("action", width=120, minwidth=120)
        tree.column("details", width=350, minwidth=200)

        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview",
                        background=CARD_BG,
                        foreground=TEXT_PRIMARY,
                        fieldbackground=CARD_BG,
                        font=("Courier New", 9))
        style.configure("Treeview.Heading",
                        background=BG_SECONDARY,
                        foreground=TEXT_PRIMARY,
                        font=("Courier New", 10, "bold"))
        style.map("Treeview",
                 background=[("selected", ACCENT)],
                 foreground=[("selected", "#ffffff")])

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load transactions for current user
        self._load_transactions(tree)

        return screen

    def _load_transactions(self, tree):
        """Load and display transactions for the current user"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)

        # Get all decrypted logs
        all_logs = read_decrypted_logs()

        # Filter logs for current user
        user_logs = []
        current_username = self.app.client.username

        for log_line in all_logs:
            if "[Could not decrypt" in log_line:
                continue

            try:
                # Parse log format: "timestamp | username | action | details"
                parts = log_line.split(" | ")
                if len(parts) >= 3:
                    timestamp = parts[0]
                    username = parts[1]
                    action = parts[2]
                    details = parts[3] if len(parts) > 3 else ""

                    if username == current_username:
                        user_logs.append((timestamp, action, details))
            except:
                continue

        # Sort by timestamp (newest first)
        user_logs.sort(key=lambda x: x[0], reverse=True)

        # Add to treeview
        for timestamp, action, details in user_logs:
            # Format action for display
            display_action = action.replace("_", " ").title()

            # Format details
            if not details:
                display_details = "N/A"
            elif "Deposited" in details:
                display_details = f"Amount: {details.split()[-1]}"
            elif "Withdrew" in details:
                display_details = f"Amount: {details.split()[-1]}"
            elif "New balance" in details:
                display_details = f"Balance: {details.split()[-1]}"
            else:
                display_details = details

            tree.insert("", "end", values=(timestamp, display_action, display_details))

        # If no transactions
        if not user_logs:
            tree.insert("", "end", values=("No transactions found", "", ""))

