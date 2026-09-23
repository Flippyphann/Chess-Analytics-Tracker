import chess


# Checks if the player's move matches Stockfish's best move.
def is_best_move(board: chess.Board, move: str, best_move: chess.Move) -> bool:
    played_move = board.parse_san(move)

    return played_move == best_move

# Classifies a move based on evaluation loss.
def classify_move(evaluation_loss: float) -> str:
    if evaluation_loss < 0.50:
        return "good"
    elif evaluation_loss < 1.00:
        return "inaccuracy"
    elif evaluation_loss < 2.00:
        return "mistake"
    else:
        return "blunder"

# Checks if a move caused a significant evaluation change.
def is_critical(evaluation_change: float) -> bool:
    return abs(evaluation_change) >= 1.00

# Checks if the player's move is one of Stockfish's top 3 moves.
def is_top_3_move(board: chess.Board, move: str, top_moves: list[chess.Move]) -> bool:
    played_move = board.parse_san(move)

    return played_move in top_moves

# Checks if the player's move is one of Stockfish's top 5 moves.
def is_top_5_move(board: chess.Board, move: str, top_moves: list[chess.Move]) -> bool:
    played_move = board.parse_san(move)

    return played_move in top_moves

# Checks if the player's position improved after the move.
def is_improvement(evaluation_change: float) -> bool:
    return evaluation_change > 0

# Checks if the player's position worsened after the move.
def is_worsening(evaluation_change: float) -> bool:
    return evaluation_change < 0

# Checks if the player's move is a blunder.
def is_blunder(evaluation_loss: float) -> bool:
    return evaluation_loss >= 2
