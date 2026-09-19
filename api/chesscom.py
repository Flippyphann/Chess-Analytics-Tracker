import requests

BASE_URL = "https://api.chess.com/pub"

HEADERS = {
    "User-Agent": "ChessDNA/1.0"
}

# Gets player information.
def get_player(username: str) -> dict:
    url = f"{BASE_URL}/player/{username}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()

# Gets the player's game archive URLs.
def get_archives(username: str) -> list:
    url = f"{BASE_URL}/player/{username}/games/archives"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    data = response.json()
    return data["archives"]

# Grabs games from an archive.
def get_games_from_archive(archive_url: str) -> dict:
    response = requests.get(archive_url, headers=HEADERS)
    response.raise_for_status()

    data = response.json()
    return data["games"]


