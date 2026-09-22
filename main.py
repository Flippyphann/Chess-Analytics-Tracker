import json


from parser.pgn_parser import parse_game

USERNAME = "phillipphan11"

# Loads the raw games.
with open(f"data/raw/{USERNAME}.json", "r", encoding = "utf-8") as file:
    games = json.load(file)

# Parses the games.
parsed_games = []

for game_data in games:
    game = parse_game(game_data["pgn"])
    parsed_games.append(game)


