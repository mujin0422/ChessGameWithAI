 # Hiển thị bàn cờ

import tkinter as tk
from tkinter import messagebox
from ChessGameWithAI.auth.auth import register_user, login_user

def register():
    username = entry_username.get()
    password = entry_password.get()

    if register_user(username, password):
        messagebox.showinfo("Success", "Đăng ký thành công!")
    else:
        messagebox.showerror("Error", "Tài khoản đã tồn tại!")

def login():
    username = entry_username.get()
    password = entry_password.get()

    if login_user(username, password):
        messagebox.showinfo("Success", "Đăng nhập thành công!")
    else:
        messagebox.showerror("Error", "Sai tài khoản hoặc mật khẩu!")

# Giao diện Tkinter
root = tk.Tk()
root.title("Login/Register")

tk.Label(root, text="Username:").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Register", command=register).pack()
tk.Button(root, text="Login", command=login).pack()

root.mainloop()
