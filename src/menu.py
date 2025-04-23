import tkinter as tk
from tkinter import PhotoImage
import const  
import os

class MenuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CHESS MENU")
        self.root.configure(bg="#222222")
        self.selected_mode = None

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons")
        chess_icon = PhotoImage(file=os.path.join(icon_path, "chess.png"))
        self.root.tk.call('wm', 'iconphoto', self.root._w, chess_icon)
        self.icon_bot = PhotoImage(file=os.path.join(icon_path, "bot.png"))
        self.icon_practice = PhotoImage(file=os.path.join(icon_path, "practice.png"))
        self.icon_exit = PhotoImage(file=os.path.join(icon_path, "exit.png"))

        # Sử dụng kích thước từ const.py
        root.update_idletasks()
        w = const.SCREEN_WIDTH
        h = const.SCREEN_HEIGHT
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - w) // 2
        y = (screen_height - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")

        frame = tk.Frame(root, bg="#222222")
        frame.pack(expand=True)

        title = tk.Label(frame, text="CHESS GAME", font=("Arial", 60, "bold"),
                         fg="white", bg="#222222")
        title.pack(pady=(40, 60))

        self.create_button(frame, "PLAY BOT", lambda: self.select_mode(True), self.icon_bot)
        self.create_button(frame, "PRACTICE", lambda: self.select_mode(False), self.icon_practice)
        self.create_button(frame, "EXIT", root.quit, self.icon_exit)


    def on_enter(self, e):
        e.widget.config(bg="#FF1493")  
    def on_leave(self, e):
        e.widget.config(bg="#228B22") 

    def create_button(self, parent, text, command, icon=None):
        btn = tk.Button(parent, text=text, command=command,
                        width=360, height=40,
                        font=("Arial", 20, "bold"),
                        bg="#228B22", fg="white",
                        image=icon, compound="left",
                        activebackground="#45a049", activeforeground="white",
                        relief="raised", bd=3,
                        anchor="w", padx=20)
        btn.bind("<Enter>", self.on_enter)  
        btn.bind("<Leave>", self.on_leave)  
        btn.pack(pady=10)


    def select_mode(self, ai_enabled):
        self.selected_mode = ai_enabled
        self.root.destroy()

def get_game_mode():
    root = tk.Tk()
    menu = MenuUI(root)
    root.mainloop()
    return menu.selected_mode
