import tkinter as tk
from tkinter import messagebox
import time

from frontend.client import BankingClient
from frontend.theme import BG_PRIMARY, SUCCESS, ERROR, ACCENT
from frontend.views.login_view import LoginView
from frontend.views.register_view import RegisterView
from frontend.views.dashboard_view import DashboardView
from frontend.views.transactions_view import TransactionsView
from frontend.views.deposit_view import DepositView
from frontend.views.balance_view import BalanceView
from frontend.views.receipt_popup import ReceiptPopup


class BankingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vault — Secure Banking")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(False, False)

        self.client = BankingClient()
        self.current_screen = None

        self.username_entry = None
        self.password_entry = None
        self.login_error_label = None

        self.register_username_entry = None
        self.register_password_entry = None
        self.register_confirm_entry = None
        self.register_result_label = None
        self.register_strength_label = None

        self.deposit_entry = None
        self.deposit_entry_frame = None
        self.deposit_result_label = None

        self.balance_display = None
        self.balance_timestamp = None
        self.balance_status_label = None

        self.show_login_screen()

    # -----------------------------
    # SCREEN SWITCHING
    # -----------------------------
    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()
        self.root.unbind("<Return>")

    def show_login_screen(self):
        self.clear_screen()
        self.current_screen = LoginView(self).build()

    def show_register_screen(self):
        self.clear_screen()
        self.current_screen = RegisterView(self).build()

    def show_dashboard(self):
        self.clear_screen()
        self.current_screen = DashboardView(self).build()

    def show_deposit_screen(self):
        self.clear_screen()
        self.current_screen = DepositView(self).build()

    def show_balance_screen(self):
        self.clear_screen()
        self.current_screen = BalanceView(self).build()

    def show_transactions_screen(self):
        self.clear_screen()
        self.current_screen = TransactionsView(self).build()

    # -----------------------------
    # LOGIN
    # -----------------------------
    def handle_login(self):
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
        except Exception as e:
            messagebox.showerror("UI Error", f"Could not read login fields: {e}")
            return

        if not username or not password:
            msg = "Please enter both username and password."
            if self.login_error_label:
                self.login_error_label.config(text=msg)
            else:
                messagebox.showwarning("Missing Info", msg)
            return

        if self.login_error_label:
            self.login_error_label.config(text="Connecting...")
        self.root.update()

        try:
            success, message = self.client.login(username, password)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not reach server:\n{e}")
            if self.login_error_label:
                self.login_error_label.config(text=f"Connection failed: {e}")
            return

        print(f"[LOGIN] success={success}  message={message}")

        if success:
            self.show_dashboard()
        else:
            if self.login_error_label:
                self.login_error_label.config(text=f"✕  {message}")
            messagebox.showerror("Login Failed", message)

    # -----------------------------
    # REGISTER
    # -----------------------------
    def handle_register(self):
        try:
            username = self.register_username_entry.get().strip()
            password = self.register_password_entry.get().strip()
            confirm = self.register_confirm_entry.get().strip()
        except Exception as e:
            messagebox.showerror("UI Error", f"Could not read register fields: {e}")
            return

        def set_error(msg):
            messagebox.showerror("Registration Error", msg)

        def set_success(msg):
            if self.register_result_label:
                self.register_result_label.config(text=f"✓  {msg}", fg=SUCCESS)
                self.root.update()

        if not username or not password or not confirm:
            set_error("All fields are required.")
            return

        if len(username) < 3:
            set_error("Username must be at least 3 characters.")
            return

        if len(password) < 4:
            set_error("Password must be at least 4 characters.")
            return

        if password != confirm:
            set_error("Passwords do not match.")
            return

        try:
            success, message = self.client.register(username, password)
            print(f"[REGISTER] success={success}  message={message}")
            if success:
                set_success("Account created successfully!")
                # Redirect immediately instead of after delay
                self.root.after(1000, self.show_login_screen)
            else:
                set_error(message)
        except Exception as e:
            print(f"[REGISTER] Exception: {e}")
            set_error(f"Registration failed: {str(e)}")

    # -----------------------------
    # DEPOSIT
    # -----------------------------
    def handle_deposit(self):
        try:
            amount = self.deposit_entry.get().strip()
        except Exception as e:
            messagebox.showerror("UI Error", str(e))
            return

        if not amount:
            self.deposit_result_label.config(text="✕  Please enter an amount.", fg=ERROR)
            return

        try:
            value = float(amount)
            if value <= 0:
                self.deposit_result_label.config(text="✕  Amount must be greater than $0.", fg=ERROR)
                return
        except ValueError:
            self.deposit_result_label.config(text="✕  Please enter a valid number.", fg=ERROR)
            return

        self.deposit_result_label.config(text="Processing...", fg=ACCENT)
        self.root.update()

        try:
            success, message = self.client.deposit(amount)
        except Exception as e:
            messagebox.showerror("Deposit Error", str(e))
            return

        print(f"[DEPOSIT] success={success}  message={message}")

        if success:
            self.deposit_result_label.config(text="✓  Deposit successful.", fg=SUCCESS)
            self.deposit_entry.delete(0, tk.END)
            ReceiptPopup(self.root, action="Deposit", amount=value, success=True, server_reply=message)
        else:
            self.deposit_result_label.config(text=f"✕  {message}", fg=ERROR)
            ReceiptPopup(self.root, action="Deposit", amount=value, success=False, server_reply=message)

    # -----------------------------
    # BALANCE
    # -----------------------------
    def handle_balance_refresh(self):
        if self.balance_display is None:
            return

        if self.balance_status_label:
            self.balance_status_label.config(text="Fetching...")
        self.balance_display.config(text="$ ···", fg=ACCENT)
        self.root.update()

        try:
            success, message = self.client.check_balance()
        except Exception as e:
            self.balance_display.config(text="$ --", fg="#ef4444")
            if self.balance_status_label:
                self.balance_status_label.config(text=f"Error: {e}")
            return

        print(f"[BALANCE] success={success}  message={message}")

        if success:
            try:
                value = float(message.replace("$", "").replace(",", "").strip())
                display = f"$ {value:,.2f}"
            except (ValueError, AttributeError):
                display = f"$ {message}"

            self.balance_display.config(text=display, fg="#6ee7b7")
            if self.balance_timestamp:
                self.balance_timestamp.config(text=f"Updated {time.strftime('%H:%M:%S')}")
            if self.balance_status_label:
                self.balance_status_label.config(text="")
        else:
            self.balance_display.config(text="$ --", fg="#ef4444")
            if self.balance_status_label:
                self.balance_status_label.config(text=f"Error: {message}")

    # -----------------------------
    # LOGOUT
    # -----------------------------
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