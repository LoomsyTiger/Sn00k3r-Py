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
gui_player1_name.grid(row=1,column=1)
gui_player1_score = ctk.CTkLabel(gui, text=f"Score: {players[1]['score']}", font=("Arial", 14))
gui_player1_score.grid(row=1,column=2)

gui_player2_name = ctk.CTkLabel(gui, text=f"{players[2]['name']}", font=("Arial", 16))
gui_player2_name.grid(row=1,column=5)
gui_player2_score = ctk.CTkLabel(gui, text=f"Score: {players[2]['name']}", font=("Arial", 14))
gui_player2_score.grid(row=1,column=6)

active_player, opponent = get_active_player()
active_player_name = players[active_player]["name"]
current_break = players[active_player]["current_break"]
opponent_name = players[opponent]["name"]
gui_message = f"{active_player_name} to break."
highest_break = ctk.CTkLabel(gui, text="Highest Break: 0", font=("Arial", 14))
highest_break.grid(row=1,column=4)

# ---
# Functions for TKinter stuff
# ---

def on_ball_click(ball_color:str):
    register_pott(ball_color)

def on_general_click(event:str):
    if event == "Foul":
        register_foul()
    elif event == "End of break":
        end_break()
    elif event == "End game":
        end_game()

def update_scores():
    gui_player1_score.configure(text=f"Score: {players[1]['score']}")
    gui_player2_score.configure(text=f"Score: {players[2]['score']}")

def update_log(fstring:str):
    game_history.append(fstring)

def create_button(gui, type:str, event:str, button_color:str, row:int, column:int):
    text_color = "White" if event not in ["Pink", "Yellow", "End game", "Red", "End of break", "Foul"] else "Black"

    if type == "Ball":
        button = ctk.CTkButton(gui, text=event, command=lambda: on_ball_click(event), fg_color=button_color, hover_color=button_color, text_color=text_color)
    elif type == "Sys":
        button = ctk.CTkButton(gui, text=event, command=lambda: on_general_click(event), fg_color=button_color, hover_color=button_color, text_color=text_color)
    
    button.grid(row=row, column=column, padx=5, pady=5)
    return button

# Create snooker ball buttons
button_red_ball = create_button(gui=gui, type="Ball", event="Red", button_color="Red", row=3, column=4)
button_yellow_ball = create_button(gui=gui, type="Ball", event="Yellow", button_color="Yellow", row=4, column=3)
button_green_ball = create_button(gui=gui, type="Ball", event="Green", button_color="Green", row=5, column=3)
button_brown_ball = create_button(gui=gui, type="Ball", event="Brown", button_color="Brown", row=6, column=3)
button_blue_ball = create_button(gui=gui, type="Ball", event="Blue", button_color="Blue", row=4, column=5)
button_pink_ball = create_button(gui=gui, type="Ball", event="Pink", button_color="Pink", row=5, column=5)
button_black_ball = create_button(gui=gui, type="Ball", event="Black", button_color="Black", row=6, column=5)

# Create general buttons
button_foul = create_button(gui=gui, type="Sys", event="Foul", button_color="White", row=8, column=3)
button_eob = create_button(gui=gui, type="Sys", event="End of break", button_color="White", row=8, column=4)
button_end_game = create_button(gui=gui, type="Sys", event="End game", button_color="Red", row=8, column=5)

# ---
# Functions for game logic
# ---

def get_ball_value(color:str):
    points = ball_values[color]
    return points

def point_addition(points:int, legality:str):
    active_player, opponent = get_active_player()
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

def register_pott(potted_ball:str):
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

def register_foul(potted_ball:str=None):
    if (potted_ball == None):
        fouled_ball = ctk.CTkInputDialog(text="What ball was on?", title="Register foul")
        fouled_ball_value = get_ball_value(fouled_ball.lower())
        penalty = point_addition(fouled_ball_value, "foul")
    else:
        fouled_ball_value = get_ball_value(potted_ball)
        penalty = point_addition(fouled_ball_value, "foul")

    update_log(f"Penalty {penalty} added to {opponent_name}.")


def end_break():
    global turn_counter, break_history
    turn_counter += 1
    if (current_break > players[active_player]["max_break"]):
        players[active_player]["max_break"] = current_break
        players[active_player]["current_break"] = 0
        break_history.clear()
        update_log(f"New highest break for {players[active_player]['name']}: {current_break} points.")
    else:
        players[active_player]["current_break"] = 0
        break_history.clear()
        update_log(f"End of break. Total score this break: {current_break}")

def respotted_black():
    global ball_count
    ball_count += 1
    update_log(f"It's a tie. Respot the black ball.")
    
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
        respotted_black()
    
def game_summary():
    update_log(f"Game over. Winner: {game_stats['winner_name']} with {game_stats['winner_score']}.\nHighest break: {game_stats['highest_break']}.")

#
# Start app
#

gui.mainloop()         
