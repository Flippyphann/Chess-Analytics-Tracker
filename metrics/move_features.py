import chess


# Checks if the player's move matches Stockfish's best move.
def is_best_move(board: chess.Board, move: str, best_move: chess.Move) -> bool:
    played_move = board.parse_san(move)

    return played_move == best_move

# Classifies a move based on evaluation loss.
def classify_move(evaluation_loss: float) -> str:
    if evaluation_loss < 0.10:
        return "best"
    elif evaluation_loss < 0.50:
        return "good"
    elif evaluation_loss < 1.00:
        return "inaccuracy"
    elif evaluation_loss < 2.00:
        return "mistake"
    else:
        return "blunder"
