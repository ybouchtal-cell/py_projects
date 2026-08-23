#---------------------------------
#log_in.page
# --------------------------------

import tkinter as tk 
from tkinter import messagebox
import csv 
import re 



# Regex for email that ends with @gmail.com
EMAIL_RE = re.compile(r'^[\w.+-]+@gmail\.com$', re.IGNORECASE)
UPPER_RE = re.compile(r'[A-Z]')
LOWER_RE = re.compile(r'[a-z]')
DIGIT_RE = re.compile(r'\d')
SPECIAL_RE = re.compile(r'[^A-Za-z0-9]')
NO_SPACE_RE = re.compile(r'^\S+$')

def validate_email(email: str):
    if not EMAIL_RE.match(email):
        return False, "Email must be in the form <name>@gmail.com (example: user@gmail.com)."
    return True, "Email OK."

def validate_password(pw: str):
    failures = []
    if len(pw) < 8:
        failures.append("Password must be at least 8 characters long.")
    if not UPPER_RE.search(pw):
        failures.append("Password must contain at least one uppercase letter (A-Z).")
    if not LOWER_RE.search(pw):
        failures.append("Password must contain at least one lowercase letter (a-z).")
    if not DIGIT_RE.search(pw):
        failures.append("Password must contain at least one digit (0-9).")
    if not SPECIAL_RE.search(pw):
        failures.append("Password must contain at least one special character (e.g. ! @ # $ % ^ & * ).")
    if not NO_SPACE_RE.match(pw):
        failures.append("Password must not contain spaces.")
    return (len(failures) == 0), failures

class Log_in :
    def __init__(self,root):
        self.root = root
        self.root.title("log_in page")
        self.root.geometry("420x260")

        self.email_label = tk.Label(self.root , text = "Email :")
        self.email_label.pack(pady=(15,0))
        self.email_entry = tk.Entry(self.root , width= 40)
        self.email_entry.pack()

        self.password_label = tk.Label(self.root , text="Password :")
        self.password_label.pack(pady=(10,0))
        self.password_entry = tk.Entry(self.root , show="*" , width =40)
        self.password_entry.pack()

        self.status_label = tk.Label(self.root , text="",fg="red")
        self.status_label.pack(pady=(10,0))

        self.submit_button = tk.Button(self.root , text="Submit" , command=self.login)
        self.submit_button.pack(pady=15)

        self.signup_button = tk.Button(self.root , text="sign up" , command=self.signup )
        self.signup_button.pack(pady=5)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        found = False
        with open("BankAccounts.csv","r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["email"] == email and row["password"] == password:
                    self.status_label.config(text="login successful", fg ="green")
                    key_code = row.get("key_code", "0000")
                    balance = row.get("balance", "0")
                    self.home(key_code, balance)
                    found = True
                    break
        if not found:
            self.status_label.config(text="login failed", fg="red")

    def signup(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("420x300")

        email_label = tk.Label(signup_window, text="New Email :")
        email_label.pack(pady=(15,0))
        email_entry = tk.Entry(signup_window, width=35)
        email_entry.pack()

        password_label = tk.Label(signup_window, text="New Password :")
        password_label.pack(pady=(10,0))
        password_entry = tk.Entry(signup_window, show="*", width=35)
        password_entry.pack()

        key_code_label = tk.Label(signup_window, text="Key Code (4 digits):")
        key_code_label.pack(pady=(10,0))
        key_code_entry = tk.Entry(signup_window, width=35)
        key_code_entry.pack()

        status_label = tk.Label(signup_window, text="", fg="blue")
        status_label.pack(pady=(10,0))

        status_button = tk.Button(signup_window, text="Submit", command=lambda: self.saver(email_entry, password_entry, key_code_entry, status_label, signup_window))
        status_button.pack(pady=10)

    def saver(self, email_entry, password_entry, key_code_entry, status_label, signup_window):
        email = email_entry.get().strip()
        password = password_entry.get()

        key_code = key_code_entry.get().strip()
        balance = "0"
        ok_email, email_msg = validate_email(email)
        ok_pw, pw_failures = validate_password(password)
        if not key_code.isdigit() or len(key_code) != 4:
            status_label.config(text="[ERROR] Key code must be 4 digits.", fg="red")
            return

        # Prepare feedback
        if not ok_email:
            status_label.config(text=f"[ERROR] {email_msg}", fg="red")
            return
        if not ok_pw:
            fail_text = "[ERROR] Password failed:\n" + "\n".join(" - " + f for f in pw_failures)
            status_label.config(text=fail_text, fg="red")
            return
        

        # All checks passed
        status_label.config(text="[OK] All checks passed. Credentials accepted.", fg="green")
        try:
            with open("BankAccounts.csv", mode="a", newline="") as csvfile:
                fieldnames = ["email", "password", "key_code", "balance"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # Write header if file is empty
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow({"email": email, "password": password, "key_code": key_code, "balance": balance})
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Success", "Credentials saved to BankAccounts.csv")
            signup_window.destroy()
        except (IOError, csv.Error) as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to save credentials: {e}")
    def home(self, key_code, balance):
        home_window = tk.Toplevel(self.root)
        home_window.title("Bank home")
        home_window.geometry("420x260")
        welcome_label = tk.Label(home_window, text="welcome to your bank account")
        welcome_label.pack(pady=20)
        balance_label = tk.Label(home_window, text=f"your balance is : {balance}$")
        balance_label.pack(pady=10)
        key_label = tk.Label(home_window, text=f"your key_code is : {key_code}")
        key_label.pack(pady=10)

        deposit_button = tk.Button(home_window, text="deposit", command=lambda: self.deposit(balance, key_code))
        deposit_button.pack(pady=5)

        # Fix typo: tk.button -> tk.Button
        withdraw_button = tk.Button(home_window, text="withdraw", command=lambda: self.with_drew(balance, key_code))
        withdraw_button.pack(pady=5)

    def deposit(self, balance, key_code):
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Deposit")
        deposit_window.geometry("420x260")
        tk.Label(deposit_window, text="enter your key_code :").pack(pady=(15,0))
        key_code_entry = tk.Entry(deposit_window, width=35)
        key_code_entry.pack()
        tk.Label(deposit_window, text="enter amount to deposit :").pack(pady=(10,0))
        deposit_entry = tk.Entry(deposit_window, width=35)
        deposit_entry.pack()
        status_label = tk.Label(deposit_window, text="", fg="red")
        status_label.pack(pady=(10,0))

        def submit_deposit():
            entered_key = key_code_entry.get().strip()
            deposit_amt = deposit_entry.get().strip()
            if entered_key != key_code:
                status_label.config(text="ERROR: wrong key code", fg="red")
                return
            try:
                deposit_amt = float(deposit_amt)
                if deposit_amt <= 0:
                    status_label.config(text="ERROR: deposit must be positive", fg="red")
                    return
            except ValueError:
                status_label.config(text="ERROR: enter a valid number", fg="red")
                return

            # Read all rows, update the matching one
            updated = False
            rows = []
            with open("BankAccounts.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["key_code"] == key_code:
                        old_balance = float(row.get("balance", "0"))
                        new_balance = old_balance + deposit_amt
                        row["balance"] = str(new_balance)
                        updated = True
                    rows.append(row)

            if updated:
                with open("BankAccounts.csv", "w", newline="") as file:
                    fieldnames = ["email", "password", "key_code", "balance"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                status_label.config(text=f"Success: new balance is {row['balance']}$", fg="green")
                deposit_window.after(1500, deposit_window.destroy)
            else:
                status_label.config(text="ERROR: Account not found", fg="red")

        submit_button = tk.Button(deposit_window, text="submit", command=submit_deposit)
        submit_button.pack(pady=10)
        exit_button = tk.Button(deposit_window, text="exit", command=deposit_window.destroy)
        exit_button.pack(pady=5)
    
    def with_drew(self, balance, key_code):
        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("420x260")
        tk.Label(withdraw_window, text="enter your key_code :").pack(pady=(15,0))
        key_code_entry = tk.Entry(withdraw_window, width=35)
        key_code_entry.pack()
        tk.Label(withdraw_window, text="enter amount to withdraw :").pack(pady=(10,0))
        withdraw_entry = tk.Entry(withdraw_window, width=35)
        withdraw_entry.pack()
        status_label = tk.Label(withdraw_window, text="", fg="red")
        status_label.pack(pady=(10,0))

        def submit_withdraw():
            entered_key = key_code_entry.get().strip()
            withdraw_amt = withdraw_entry.get().strip()
            if entered_key != key_code:
                status_label.config(text="ERROR: wrong key code", fg="red")
                return
            try:
                withdraw_amt = float(withdraw_amt)
                if withdraw_amt <= 0:
                    status_label.config(text="ERROR: invalid withdraw amount", fg="red")
                    return
            except ValueError:
                status_label.config(text="ERROR: invalid number", fg="red")
                return
            # Read all rows, update the matching one
            updated = False
            rows = []
            with open("BankAccounts.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["key_code"] == key_code:
                        old_balance = float(row.get("balance", "0"))
                        if old_balance < withdraw_amt:
                            status_label.config(text="Insufficient funds!", fg="red")
                            return
                        new_balance = old_balance - withdraw_amt
                        row["balance"] = str(new_balance)
                        updated = True
                    rows.append(row)
            if updated:
                with open("BankAccounts.csv", "w", newline="") as file:
                    fieldnames = ["email", "password", "key_code", "balance"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                status_label.config(text=f"Success: new balance is {row['balance']}$", fg="green")
                withdraw_window.after(1500, withdraw_window.destroy)
            else:
                status_label.config(text="ERROR: Account not found", fg="red")

        submit_button = tk.Button(withdraw_window, text="submit", command=submit_withdraw)
        submit_button.pack(pady=10)
        exit_button = tk.Button(withdraw_window, text="exit", command=withdraw_window.destroy)
        exit_button.pack(pady=5)



        
            



                            

                        

                    









     

    
if __name__ == "__main__":
    root = tk.Tk()
    app = Log_in(root)
    root.mainloop()