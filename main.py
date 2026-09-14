from api.chesscom import get_player, get_archives, get_games_from_archive

USERNAME = "phillipphan11"

player = get_player(USERNAME)
archives = get_archives(USERNAME)
games = get_games_from_archive(archives[0])

print(player)
print(archives)
print(games)