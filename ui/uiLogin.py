import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.database import Database
from uiGamemode import SelectGameMode
from consts import *

class LoginApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("LOGIN")
        self.root.configure(bg="#333333")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - SCREEN_WIDTH) // 2
        y = (screen_height - SCREEN_WIDTH) // 2
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{x}+{y}")

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
        tk.Label(frame, text="LOGIN", bg="#333333", fg="#FFFFFF", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        tk.Label(frame, text="Username:", bg="#333333", fg="#FFFFFF", font=("Arial", 16)).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.username_entry = tk.Entry(frame, width=30, font=("Arial", 14), bd=2, relief="solid")
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, ipady=5, sticky="ew")

        # Password
        tk.Label(frame, text="Password:", bg="#333333", fg="#FFFFFF", font=("Arial", 16)).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.password_entry = tk.Entry(frame, show="*", width=30, font=("Arial", 14), bd=2, relief="solid")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, ipady=5, sticky="ew")

        # Nút Login & Register
        login_btn = tk.Button(frame, text="Login", command=self.login, width=15, font=("Arial", 12, "bold"),
                               bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", relief="raised")
        login_btn.grid(row=3, column=0, pady=15, padx=5)

        register_btn = tk.Button(frame, text="Register", command=self.register, width=15, font=("Arial", 12, "bold"),
                                 bg="#008CBA", fg="white", activebackground="#007bb5", activeforeground="white", relief="raised")
        register_btn.grid(row=3, column=1, pady=15, padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.withdraw()  # Ẩn cửa sổ đăng nhập
            self.open_game_mode()  # Mở cửa sổ chọn chế độ chơi
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username already exists")

    def open_game_mode(self):
        game_mode_window = tk.Toplevel(self.root)
        SelectGameMode(game_mode_window) 

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
