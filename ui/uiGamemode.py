import tkinter as tk
from consts import *

class SelectGameMode:
    def __init__(self, root):
        self.root = root
        self.root.title("SELECT GAME MODE")
        self.root.configure(bg="#333333")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - SCREEN_WIDTH) // 2
        y = (screen_height - SCREEN_WIDTH) // 2
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{x}+{y}")


        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        frame = tk.Frame(root, bg="#333333")
        frame.grid(row=0, column=0, padx=20, pady=20)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        mode_ai_btn = tk.Button(frame, text="SINGLE PLAYER", command=self.play_with_ai, width=50, 
                                font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                                activebackground="#45a049", activeforeground="white", relief="raised")
        mode_ai_btn.grid(row=0, column=0, pady=10, padx=10)

        mode_pvp_btn = tk.Button(frame, text="MULTI PLAYER", command=self.play_with_user, width=50, 
                                 font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                                 activebackground="#45a049", activeforeground="white", relief="raised")
        mode_pvp_btn.grid(row=1, column=0, pady=10, padx=10)

        mode_bullet_btn = tk.Button(frame, text="BULLET CHESS", command=self.play_with_user, width=50, 
                                    font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                                    activebackground="#45a049", activeforeground="white", relief="raised")
        mode_bullet_btn.grid(row=2, column=0, pady=10, padx=10)

    def play_with_ai(self):
        print("Chơi với AI")

    def play_with_user(self):
        print("Chơi với người chơi khác")

if __name__ == "__main__":
    root = tk.Tk()
    app = SelectGameMode(root)
    root.mainloop()
