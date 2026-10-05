from models.game import Game


# Calculates the average evaluation loss across all moves.
def average_evaluation_loss(results: list[dict]) -> float:
    total_loss = 0

    for result in results:
        total_loss += result["evaluation_loss"]

    return total_loss / len(results)


# Calculates the percentage of moves that were Stockfish's best move.
def best_move_percentage(results: list[dict]) -> float:
    best_moves = 0

    for result in results:
        if result["is_best_move"]:
            best_moves += 1

    return (best_moves / len(results)) * 100


# Calculates the percentage of moves that were among Stockfish's top 3 moves.
def top_3_move_percentage(results: list[dict]) -> float:
    top_3_moves = 0

    for result in results:
        if result["is_top_3_move"]:
            top_3_moves += 1

    return (top_3_moves / len(results)) * 100


# Calculates the percentage of moves that were among Stockfish's top 5 moves.
def top_5_percentage(results: list[dict]) -> float:
    top_5_moves = 0

    for result in results:
        if result["is_top_5_move"]:
            top_5_moves += 1

    return (top_5_moves / len(results)) * 100


# Calculates the percentage of moves that were blunders.
def blunder_rate(results: list[dict]) -> float:
    blunders = 0

    for result in results:
        if result["is_blunder"]:
            blunders += 1
    return (blunders / len(results)) * 100


# Calculates the percentage of moves that were mistakes:
def mistake_rate(results: list[dict]) -> float:
    mistakes = 0

    for result in results:
        if result["move_classification"] == "mistake":
            mistakes += 1
    return (mistakes / len(results)) * 100


# Calculates the percentage of moves that were inaccuracies.
def inaccuracy_rate(results: list[dict]) -> float:
    inaccuracies = 0

    for result in results:
        if result["move_classification"] == "inaccuracy":
            inaccuracies += 1

    return (inaccuracies / len(results)) * 100


# Calculates the percentage of games won by the player.
def win_rate(games: list[Game], username: str) -> float:
    wins = 0

    for game in games:
        if game.white == username and game.result == "1-0":
            wins += 1
        elif game.black == username and game.result == "0-1":
            wins += 1

    return (wins / len(games)) * 100


# Calculates the percentage of games lost by the player.
def loss_rate(games: list[Game], username: str) -> float:
    losses = 0

    for game in games:
        if game.white == username and game.result == "0-1":
            losses += 1
        elif game.black == username and game.result == "1-0":
            losses += 1

    return (losses / len(games)) * 100


# Calculates the percentage of games drawn by the player.
def draw_rate(games: list[Game], username: str) -> float:
    draws = 0

    for game in games:
        if game.result == "1/2-1/2":
            draws += 1

    return (draws / len(games)) * 100


# Calculates the percentage of games won by the player while playing White.
def white_win_rate(games: list[Game], username: str) -> float:
    white_games = 0
    white_wins = 0

    for game in games:
        if game.white == username:
            white_games += 1

            if game.result == "1-0":
                white_wins += 1

    return (white_wins / white_games) * 100


# Calculates the percentage of games won by the player while playing Black.
def black_win_rate(games: list[Game], username: str) -> float:
    black_games = 0
    black_wins = 0

    for game in games:
        if game.black == username:
            black_games += 1

            if game.result == "0-1":
                black_wins += 1

    return (black_wins / black_games) * 100


# Calculates the average number of checks per game.
def checks_per_game(game_results: list[list[dict]]) -> float:
    total_checks = 0

    for results in game_results:
        for result in results:
            if result["is_check"]:
                total_checks += 1

    return total_checks / len(game_results)


# Calculates the percentage of games in which the player castled.
def castling_frequency(game_results: list[list[dict]]) -> float:
    games_castled = 0

    for results in game_results:
        for result in results:
            if result["is_castle"]:
                games_castled += 1
                break

    return (games_castled / len(game_results)) * 100


# Calculates the average move number on which the player castled.
def average_castling_move(game_results: list[list[dict]]) -> float:
    castling_moves = []

    for results in game_results:
        for result in results:
            if result["is_castle"]:
                castling_moves.append(result["move_number"])
                break

    return sum(castling_moves) / len(castling_moves)