import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.database import Database

class LoginApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("LOGIN")
        self.root.geometry("600x400")
        self.root.configure(bg="#333333")

        # Cấu hình để căn giữa nội dung
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Tạo Frame chứa giao diện
        frame = tk.Frame(root, bg="#333333")
        frame.grid(row=0, column=0, padx=20, pady=20)

        # Căn giữa nội dung trong frame
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Tiêu đề
        tk.Label(frame, text="LOGIN", bg="#333333", fg="#FFFFFF",font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        tk.Label(frame, text="Username:", bg="#333333", fg="#FFFFFF", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Password
        tk.Label(frame, text="Password:", bg="#333333", fg="#FFFFFF", font=("Arial", 16, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.password_entry = tk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Nút Login & Register
        tk.Button(frame, text="Login", command=self.login, width=15).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Register", command=self.register, width=15).grid(row=3, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username already exists")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
