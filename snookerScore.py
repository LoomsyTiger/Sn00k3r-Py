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

def initialize():
    print("Welcome!")
    print("Player one, add your name: ")
    players[1]["name"] = str(input())
    print("Player two, add your name: ")
    players[2]["name"] = str(input())
    match_lineup = (f"{players[1]['name']} versus {players[2]['name']}.")
    print(match_lineup)
    print(players[1]["name"] + " to break.")

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

def register_pott():
    global ball_count, break_history
    print("What color?")
    potted_ball = str(input()).lower()
    # Check if it's the first pott
    first_pott = not break_history
    # If it's not the first pott, get the previous ball
    previous_ball = (break_history[-1] if break_history else None)
    # Check if potting order is legal
    if (first_pott) or (potted_ball != previous_ball):
        points_added = get_ball_value(potted_ball)
        point_addition(points_added, "legal")
        print(f"Points added: {points_added}")
        ball_count -= 1
        break_history.append(potted_ball)
    else:
        print("Foul.")
        register_foul(potted_ball)

def register_foul(potted_ball=None):
    if (potted_ball == None):
        print("What ball was on?")
        fouled_ball = str(input()).lower()
        fouled_ball_value = get_ball_value(fouled_ball)
        penalty = point_addition(fouled_ball_value, "foul")
        print(f"{penalty} points were added for {opponent_name}")
    else:
        fouled_ball_value = get_ball_value(potted_ball)
        penalty = point_addition(fouled_ball_value, "foul")
        print(f"{penalty} points were added for {opponent_name}")

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
    
def respotted_black():
    global ball_count
    print("It's a tie! Respotted black.")
    ball_count += 1
    
def end_game():
    if players[1]["score"] > players[2]["score"]:
        return players[1]["name"], players[1]["score"], False
    elif players[1]["score"] < players[2]["score"]:
        return players[2]["name"], players[2]["score"], False
    else:
        # Tie situation
        respotted_black()
        return "Tie", None, True
    
def game_summary():
    return "Done."

initialize()

# start game
while ball_count >= 0:
    active_player, opponent = get_active_player()
    active_player_name = players[active_player]["name"]
    current_break = players[active_player]["current_break"]
    opponent_name = players[opponent]["name"]
    if (ball_count == 0):
        winner, score, is_tie = end_game()
    else:
        while True:
            print("\nCurrent scores: ")
            print(f"{players[1]['name']}: {players[1]['score']}")
            print(f"{players[2]['name']}: {players[2]['score']}")
            print(f"\nCurrent break for player {active_player_name}: {current_break}\n")
            print(f"Register action for {active_player_name}")
            print("Potted ball with 'p', foul with 'f' or miss 'm'.")
            
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
else:
    summary = game_summary()
    print(f"{summary}")
