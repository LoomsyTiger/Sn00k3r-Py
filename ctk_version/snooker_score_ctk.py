import customtkinter as ctk

# Initialize the main application window
gui = ctk.CTk()
gui.title("Snooker Scoreboard")
gui.geometry("800x600")

# ---
# Global variables and functions for game logic
# ---

ball_count = 21
turn_counter = 1
game_history = []
break_history = []

ball_values = {
    "Red": 1,
    "Yellow": 2,
    "Green": 3,
    "Brown": 4,
    "Blue": 5,
    "Pink": 6,
    "Black": 7
}
players = {
    1: {
        "name": "",
        "score": 0,
        "current_break": 0,
        "max_break": 0
    },
    2: {
        "name": "",
        "score": 0,
        "current_break": 0,
        "max_break": 0
    }
}
game_stats = {
    "winner_name": "",
    "winner_score": 0,
    "highest_break": 0
}

def get_active_player():
    global active_player, opponent
    if (turn_counter % 2 == 0):
        active_player, opponent = 1, 2
        return active_player, opponent
    else:
        active_player, opponent = 2, 1
        return active_player, opponent

# ---
# Initialize game with player info
# ---

def initialize():
    dialog = ctk.CTkInputDialog(text="Type your name", title="Player 1")
    players[1]["name"] = dialog.get_input()
    dialog = ctk.CTkInputDialog(text="Type your name", title="Player 2")
    players[2]["name"] = dialog.get_input()
    # match_lineup = (f"{players[1]['name']} versus {players[2]['name']}.")

initialize()

# Player information labels
gui_player1_name = ctk.CTkLabel(gui, text=f"{players[1]['name']}", font=("Arial", 16))
gui_player1_name.pack(pady=10)
gui_player1_score = ctk.CTkLabel(gui, text=f"Score: {players[1]['score']}", font=("Arial", 14))
gui_player1_score.pack()

gui_player2_name = ctk.CTkLabel(gui, text=f"{players[2]['name']}", font=("Arial", 16))
gui_player2_name.pack(pady=10)
gui_player2_score = ctk.CTkLabel(gui, text=f"Score: {players[2]['name']}", font=("Arial", 14))
gui_player2_score.pack()

active_player, opponent = get_active_player()
active_player_name = players[active_player]["name"]
current_break = players[active_player]["current_break"]
opponent_name = players[opponent]["name"]
gui_message = f"{active_player_name} to break."
highest_break = ctk.CTkLabel(gui, text="Highest Break: 0", font=("Arial", 14))
highest_break.pack(pady=20)

# ---
# Functions for TKinter stuff
# ---

def on_ball_click(ball_color):
    register_pott(ball_color)

def on_general_click(label):
    if label == "Foul":
        register_foul()
    elif label == "End of break":
        end_break()

def create_ball_button(ball_color, color):
    button = ctk.CTkButton(gui, text=ball_color, command=lambda: on_ball_click(ball_color), fg_color=color, hover_color="White")
    button.pack(pady=5)

def create_general_button(label, color):
    button = ctk.CTkButton(gui, text=label, command=lambda: on_general_click(label), fg_color=color, hover_color="White", compound="bottom")
    button.pack(pady=5)

def update_scores():
    gui_player1_score.configure(text=f"Score: {players[1]['score']}")
    gui_player2_score.configure(text=f"Score: {players[2]['score']}")

def update_log(fstring):
    game_history.append(fstring)

# Create snooker ball buttons
create_ball_button("Red", "Red")
create_ball_button("Yellow", "Yellow")
create_ball_button("Green", "Green")
create_ball_button("Brown", "Brown")
create_ball_button("Blue", "Blue")
create_ball_button("Pink", "Pink")
create_ball_button("Black", "Black")

# Create general buttons
create_general_button("Foul", "Red")
create_general_button("End of break", "White")
create_general_button("End game now", "Red")

# ---
# Functions for game logic
# ---

def get_ball_value(color):
    points = ball_values[color]
    return points

def point_addition(points, legality):
    if (legality == "legal"):
        players[active_player]["score"] += points
        players[active_player]["current_break"] += points
        update_scores()
    elif (legality == "foul"):
        # snooker has a minimum penalty of 4 points        
        if (points < 4):
            players[opponent]["score"] += 4
            update_scores()
            return 4
        elif (points >= 4):
            players[opponent]["score"] += points
            update_scores()
            return points

def register_pott(potted_ball):
    global ball_count, break_history
    first_pott = not break_history
    previous_ball = (break_history[-1] if break_history else None)
    if (first_pott) or (potted_ball != previous_ball):
        points_added = get_ball_value(potted_ball)
        point_addition(points_added, "legal")
        ball_count -= 1
        break_history.append(potted_ball)
        update_log(f"{potted_ball} potted by {active_player_name}.")
    else:
        register_foul(potted_ball)

    if ball_count == 0:
        end_game()

def register_foul(potted_ball=None):
    if (potted_ball == None):
        fouled_ball = ctk.CTkInputDialog(text="What ball was on?", title="Register foul")
        fouled_ball_value = get_ball_value(fouled_ball.lower())
        penalty = point_addition(fouled_ball_value, "foul")
        return penalty
    else:
        fouled_ball_value = get_ball_value(potted_ball)
        penalty = point_addition(fouled_ball_value, "foul")
        return penalty

def end_break():
    global turn_counter, break_history
    turn_counter += 1
    if (current_break > players[active_player]["max_break"]):
        players[active_player]["max_break"] = current_break
        players[active_player]["current_break"] = 0
        break_history.clear()
        update_log(f"New highest break for {players[active_player]['name']} {current_break} points.")
    else:
        players[active_player]["current_break"] = 0
        break_history.clear()
        update_log(f"End of break. Points: {current_break}")

def respotted_black():
    return
    
def end_game():
    if players[1]["score"] > players[2]["score"]:
        game_stats["winner_name"] = players[1]["name"]
        game_stats["winner_score"] = players[1]["score"]
        game_summary()
    elif players[1]["score"] < players[2]["score"]:
        game_stats["winner_name"] = players[2]["name"]
        game_stats["winner_score"] = players[2]["score"]
        game_summary()
    else:
        return "Tie", None, True
    
def game_summary():
    update_log(f"Game over. Winner: {game_stats['winner_name']} with {game_stats['winner_score']}.\nHighest break: {game_stats['highest_break']}.")

#
# Start app
#

gui.mainloop()         
