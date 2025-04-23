import tkinter as tk
import const  

class MenuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CHESS MENU")
        self.root.configure(bg="#333333")
        self.selected_mode = None

        # Sử dụng kích thước từ const.py
        root.update_idletasks()
        w = const.SCREEN_WIDTH
        h = const.SCREEN_HEIGHT
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - w) // 2
        y = (screen_height - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")

        frame = tk.Frame(root, bg="#333333")
        frame.pack(expand=True)

        title = tk.Label(frame, text="CHESS", font=("Arial", 48, "bold"),
                         fg="white", bg="#333333")
        title.pack(pady=(40, 60))

        self.create_button(frame, "PLAY VS COMPUTER", lambda: self.select_mode(True))
        self.create_button(frame, "MULTIPLAYER", lambda: self.select_mode(False))
        self.create_button(frame, "EXIT", root.quit)

    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command,
                        width=30, height=2,
                        font=("Arial", 14, "bold"),
                        bg="#4CAF50", fg="white",
                        activebackground="#45a049", activeforeground="white",
                        relief="raised", bd=3)
        btn.pack(pady=10)

    def select_mode(self, ai_enabled):
        self.selected_mode = ai_enabled
        self.root.destroy()

def get_game_mode():
    root = tk.Tk()
    menu = MenuUI(root)
    root.mainloop()
    return menu.selected_mode
