from api.chesscom import get_player, get_archives

USERNAME = "phillipphan11"

player = get_player(USERNAME)
games = get_archives(USERNAME)

print(player)
print(games)