import customtkinter as ctk
import snooker_score_ctk as score

class SnookerUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Snooker Scoreboard")
        self.geometry("800x600")

        # Player information
        self.player1_name = ctk.CTkLabel(self, text="Player 1", font=("Arial", 16))
        self.player1_name.pack(pady=10)

        self.player1_score = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 14))
        self.player1_score.pack()

        self.player2_name = ctk.CTkLabel(self, text="Player 2", font=("Arial", 16))
        self.player2_name.pack(pady=10)

        self.player2_score = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 14))
        self.player2_score.pack()

        self.highest_break = ctk.CTkLabel(self, text="Highest Break: 0", font=("Arial", 14))
        self.highest_break.pack(pady=20)

        # Snooker balls as buttons
        self.create_ball_button("Red", "red")
        self.create_ball_button("Yellow", "yellow")
        self.create_ball_button("Green", "green")
        self.create_ball_button("Brown", "brown")
        self.create_ball_button("Blue", "blue")
        self.create_ball_button("Pink", "pink")
        self.create_ball_button("Black", "black")

    def create_ball_button(self, color_name, color):
        button = ctk.CTkButton(self, text=color_name, command=lambda: self.on_ball_click(color), fg_color=color, hover_color=color)
        button.pack(pady=5)

    def on_ball_click(self, color):
        # Logic when a ball is clicked
        if color == "Red":
            score.register_pott

if __name__ == "__main__":
    app = SnookerUI()
    app.mainloop()
