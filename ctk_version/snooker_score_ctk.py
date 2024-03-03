import customtkinter as ctk

# ---
# Global variables for game logic
# ---

ball_count = 21
turn_counter = 1
break_history = []

ball_values = {
    "red": 1,
    "yellow": 2,
    "green": 3,
    "brown": 4,
    "blue": 5,
    "pink": 6,
    "black": 7
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

# ---
# GUI Setup in CustomTkinter
# ---

# Initialize the main application window
gui = ctk.CTk()
gui.title("Snooker Scoreboard")
gui.geometry("800x600")

# Handle ball click
def on_ball_click(ball_color):
    register_pott(ball_color)

def on_other_click(label):
    if label == "Foul":
        register_foul()
    elif label == "End of break":
        end_break()

# Create ball button
def create_ball_button(ball_color, color):
    button = ctk.CTkButton(gui, text=ball_color, command=lambda: on_ball_click(ball_color), fg_color=color, hover_color=color)
    button.pack(pady=5)

# Create other button
def create_other_button(label, color):
    button = ctk.CTkButton(gui, text=label, command=lambda: on_other_click(label), fg_color=color, hover_color=color)
    button.pack(pady=5)

# Player information labels
gui_player1_name = ctk.CTkLabel(gui, text="Player 1", font=("Arial", 16))
gui_player1_name.pack(pady=10)
gui_player1_score = ctk.CTkLabel(gui, text="Score: 0", font=("Arial", 14))
gui_player1_score.pack()

gui_player2_name = ctk.CTkLabel(gui, text="Player 2", font=("Arial", 16))
gui_player2_name.pack(pady=10)
gui_player2_score = ctk.CTkLabel(gui, text="Score: 0", font=("Arial", 14))
gui_player2_score.pack()

highest_break = ctk.CTkLabel(gui, text="Highest Break: 0", font=("Arial", 14))
highest_break.pack(pady=20)

# Create snooker ball buttons
create_ball_button("Red", "Red")
create_ball_button("Yellow", "Yellow")
create_ball_button("Green", "Green")
create_ball_button("Brown", "Brown")
create_ball_button("Blue", "Blue")
create_ball_button("Pink", "Pink")
create_ball_button("Black", "Black")

# Create other buttons
create_other_button("Foul", "Red")
create_other_button("End of break", "White")


# ---
# Functions for game logic
# ---

def initialize():
    dialog = ctk.CTkInputDialog(text="Type your name", title="Player 1")
    players[1]["name"] = dialog.get_input()
    dialog = ctk.CTkInputDialog(text="Type your name", title="Player 2")
    players[2]["name"] = dialog.get_input()
    # match_lineu   p = (f"{players[1]['name']} versus {players[2]['name']}.")

def get_ball_value(color):
    points = ball_values[color.lower()]
    return points

def get_active_player():
    global active_player, opponent
    if (turn_counter % 2 == 0):
        active_player, opponent = 1, 2
        return active_player, opponent
    else:
        active_player, opponent = 2, 1
        return active_player, opponent

def point_addition(points, legality):
    if (legality == "legal"):
        players[active_player]["score"] += points
        players[active_player]["current_break"] += points
        return points
    elif (legality == "foul"):
        # snooker has a minimum penalty of 4 points        
        if (points < 4):
            players[opponent]["score"] += 4
            return 4
        elif (points >= 4):
            players[opponent]["score"] += points
            return points

def register_pott(potted_ball):
    global ball_count, break_history
    # Check if it's the first pott
    first_pott = not break_history
    # If it's not the first pott, get the previous ball
    previous_ball = (break_history[-1] if break_history else None)
    # Check if potting order is legal
    if (first_pott) or (potted_ball != previous_ball):
        points_added = get_ball_value(potted_ball)
        point_addition(points_added, "legal")
        ball_count -= 1
        break_history.append(potted_ball)
    else:
        register_foul(potted_ball)

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

def end_break(eob_score):
    global turn_counter, break_history
    turn_counter += 1
    if (current_break > players[active_player]["max_break"]):
        players[active_player]["max_break"] = eob_score
        players[active_player]["current_break"] = 0
        break_history.clear()
        return (f"New highest break for {players[active_player]['name']} {eob_score} points.")
    else:
        players[active_player]["current_break"] = 0
        break_history.clear()
        return (f"End of break. Points: {eob_score}")
    
def end_game():
    if players[1]["score"] > players[2]["score"]:
        return players[1]["name"], players[1]["score"], False
    elif players[1]["score"] < players[2]["score"]:
        return players[2]["name"], players[2]["score"], False
    else:
        # Tie situation
        return "Tie", None, True
    
def game_summary():
    return "Done."

# ---
# Starting game
# ---

initialize()

active_player, opponent = get_active_player()
active_player_name = players[active_player]["name"]
current_break = players[active_player]["current_break"]
opponent_name = players[opponent]["name"]

gui.mainloop()
if (ball_count == 0):
    winner, score, is_tie = end_game()
    if is_tie == True:
        ball_count += 1
else:
    while True:
        action = input().lower()
        if action == "p":
            prev_potted_ball = register_pott()
            break
        elif action == "f":
            register_foul()
            if input("End of break? y or n: ").lower() == "y":
                print(end_break(current_break))
                break
        elif action == "m":
            print(end_break(current_break))
            break
