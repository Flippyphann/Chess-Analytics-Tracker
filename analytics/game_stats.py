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


# Calculates the percentage of moves that were critical.
def critical_move_rate(results: list[dict]) -> float:
    critical_moves = 0

    for result in results:
        if result["is_critical"]:
            critical_moves += 1

    return (critical_moves / len(results)) * 100


# Calculates the percentage of critical moves that improved the player's position.
def critical_improvement_rate(results: list[dict]) -> float:
    critical_moves = 0
    critical_improvements = 0

    for result in results:
        if result["is_critical"]:
            critical_moves += 1

            if result["is_improvement"]:
                critical_improvements += 1

    return (critical_improvements / critical_moves) * 100


# Calculates the percentage of critical moves that worsened the player's position.
def critical_worsening_rate(results: list[dict]) -> float:
    critical_moves = 0
    critical_worsening = 0

    for result in results:
        if result["is_critical"]:
            critical_moves += 1

            if result["is_worsening"]:
                critical_worsening += 1

    return (critical_worsening / critical_moves) * 100


# NOTE: most of these have to be considered as both from the dark and light pieces respectively

## Create opening/middlegame/endgame metrics
## Create an aggression index (sacrifices, attacking moves, checks played -> per total moves)
## Openings faced (and winrate versus)
## Openings used
## Loss due to/ win due to
## Find how much time is used for each move: clock()
## Find how long is takes the user to get to -1 or -2 evaluation
## What percentage of games reach endgame
## Depth of opening (if played)
## Number of mistakes as time dwindles down?
## Accuracy in time pressure
## Find if spending more time on a move makes a difference for the user in terms of accuracy
## Missed tactics?

#    DEFINE TACTIC      #
## Tactical opportunities created/found
## Tactical findings -> converted to win
## Figure out if user has a positional or tactical preference in playstyle

## Pieces left hanging
## Pieces left hanging by opponent, but wasn't captured
## Compare doubled pawns versus user's win rate
## Compared passed pawns versus user's win rate
## Winrate of player when down -2 evaluation at any point in the game
## Winrate of player when up +2 evaluation at any points in the game
## Winrate as the first player to reach an 'advantage' (like +0.5 or 1)
## ^^ How quickly did the user lose this advantage, in games that this did happen.
## ^^ If so, how often did the user recover from their mistakes
## How often does the user punish mistakes made by the opponent
## Include opponents metrics alongside the user, sort of like leetify and faceit stats for cs2.


# Not as important *
## piece activity/ king safety/ center control
## Find maximum evaluation advantage reached

## Average evaluation after leaving theory

## winrate when taken out of opening theory/ prep.
## Opening diversity
## Endgame winrate
## Drawn endgames per total endgames
## Lost endgames won (losing position objectively to winning)
## Tablebase accuracy and tablebase conversion

## Find tendency to make mistakes in winning positions
## Accuracy against higher rated player
## Accuracy against 'more games played recently' player


## Risk tolerance
## Material imbalance frequency
## Draw rate per total games played
## "Comeback" rate after worse position
## "ACPL" over last 100 games


## Track opening theory and endgame conversion growth
## Largest evaluation swing of the game
## Win probability over time
## Create a 'game complexity score'
## Track volatility (how often did the evaluation change dramatically)

# BINARY METRICS #
## Were queens traded during the game?
## Stalemates per total games
## Stalemates caused per total games
## Was opponent rated higher or lower



# EXTRA/FUN METRICS #
## Time of day of game played: clock()
## Self-initiated trading per trades played
## Mentioned already, but does time control affect the user
## Whatever this means: Do you choose sharp or simple continuations
## Whatever this means: How well your pieces support each other
## Number of moves forcing difficult defensive responses
## Value generated per move by each piece
## Performance in equal positions under one minute remaining




#    GOALS     #
## Can this program give a concurrent (to a ongoing chess game) percent chance of winning or losing based on the
## user's previous data. Like it starts at 50/50 but based on if the user sucks at the opening, or doubled their pawns,
## or created a tactical edge, their percentage would go up and down as they make their move. This would be different
## from the evaluation bar in chess.com because it factors in the player's actual strengths and weaknesses, not just
## what the engine thinks is a won or lost position.


## Create an 'mbti'-type thing for the player's chess.com stats. This would include this like positional/tactical player,
## passive/aggresive, clutch/not clutch, things like that. It would be a fun way to measure player's playstyle

## In addition to the idea above, I was thinking to make something similar but unrelated to mbti. It's something that
## derived from poker, where very player can be categorized into 4 animals: monkey, fish, etc. Thia is a lessered version
## of the mbti idea, but maybe it could be better for the project idk. The app i use for poker is called offsuit and it
## has a lot of cool data and metrics for poker that I want to implement to my project.





