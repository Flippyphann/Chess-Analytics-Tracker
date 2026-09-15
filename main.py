import json

from api.chesscom import get_player, get_archives, get_games_from_archive

USERNAME = "phillipphan11"

player = get_player(USERNAME)
archives = get_archives(USERNAME)

all_games = []

for archive in archives:
    games = get_games_from_archive(archive)
    all_games.extend(games)

print(f"Total games: {len(all_games)}")

with open(f"data/raw/{USERNAME}.json", "w", encoding="utf-8") as file:
    json.dump(all_games, file, indent=2)


print(player)
print(archives)
