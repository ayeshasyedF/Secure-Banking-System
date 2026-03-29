import tkinter as tk
from tkinter import messagebox

from frontend.client import BankingClient
from frontend.theme import BG_PRIMARY, SUCCESS, ERROR
from frontend.views.login_view import LoginView
from frontend.views.dashboard_view import DashboardView
from frontend.views.deposit_view import DepositView


class BankingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Banking ATM")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(False, False)

        self.client = BankingClient()
        self.current_screen = None

        # Widgets that views create and handlers use later
        self.username_entry = None
        self.password_entry = None
        self.deposit_entry = None
        self.deposit_result_label = None

        self.show_login_screen()

    # -----------------------------
    # SCREEN SWITCHING
    # -----------------------------
    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()

    def show_login_screen(self):
        self.clear_screen()
        self.current_screen = LoginView(self).build()

    def show_dashboard(self):
        self.clear_screen()
        self.current_screen = DashboardView(self).build()

    def show_deposit_screen(self):
        self.clear_screen()
        self.current_screen = DepositView(self).build()

    # -----------------------------
    # EVENT HANDLERS
    # -----------------------------
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Missing Information", "Please enter both username and password.")
            return

        success, message = self.client.login(username, password)

        if success:
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", message)

    def handle_deposit(self):
        amount = self.deposit_entry.get().strip()

        if not amount:
            messagebox.showerror("Missing Amount", "Please enter an amount.")
            return

        try:
            value = float(amount)
            if value <= 0:
                messagebox.showerror("Invalid Amount", "Amount must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number.")
            return

        success, message = self.client.deposit(amount)

        if success:
            self.deposit_result_label.config(
                text=f"Deposit successful.\nServer reply: {message}",
                fg=SUCCESS
            )
            self.deposit_entry.delete(0, tk.END)
        else:
            self.deposit_result_label.config(
                text=f"Deposit failed.\n{message}",
                fg=ERROR
            )

    def handle_logout(self):
        try:
            self.client.exit()
        except Exception:
            pass

        self.client = BankingClient()
        self.show_login_screen()


def main():
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()