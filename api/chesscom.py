import requests

BASE_URL = "https://api.chess.com/pub"

HEADERS = {
    "User-Agent": "ChessDNA/1.0"
}

def get_player(username: str) -> dict:
    url = f"{BASE_URL}/player/{username}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()

def get_archives(username: str) -> list:
    url = f"{BASE_URL}/player/{username}/games/archives"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    data = response.json()
    return data["archives"]

