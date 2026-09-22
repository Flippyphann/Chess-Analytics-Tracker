import chess
import chess.engine
from models.game import Game
from metrics.move_features import is_best_move, classify_move, is_critical


STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"


# Starts the Stockfish engine.
def create_engine():
    return chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Analyzes the current position on the board.
def analyze_position(engine, board: chess.Board, perspective: chess.Color):
    result = engine.analyse(
        board,
        chess.engine.Limit(depth=15)
    )

    # Grabs the best move recommended by Stockfish's principal variation (PV).
    best_move = result["pv"][0]

    # Gets the evaluation from the player's perspective (White/Black).
    evaluation = result["score"].pov(perspective)

    return {
        "best_move": best_move,
        "evaluation": evaluation
    }

# Analyzes every move in a game.
def analyze_game(engine, game: Game):
    board = chess.Board()
    results = []

    for move in game.moves:

        # Analyzes the position before the move.
        result_before = analyze_position(engine, board, board.turn)

        # Checks if played move is best move recommended by engine.
        is_best = is_best_move(
            board,
            move.san,
            result_before["best_move"]
        )

        # Plays the player's move on the board.
        board.push_san(move.san)

        # Analyzes the position after the move.
        result_after = analyze_position(engine, board, not board.turn)

        # Calculates how much the evaluation changed, in pawns.
        evaluation_change = (
            result_after["evaluation"].score(mate_score=100000)
            - result_before["evaluation"].score(mate_score=100000)
        ) / 100

        # Gets the absolute evaluation change.
        evaluation_loss = abs(evaluation_change)

        # Classifies the move based on evaluation loss.
        move_classification = classify_move(evaluation_loss)

        # Checks if the move caused a significant evaluation change.
        is_critical_move = is_critical(evaluation_change)

        results.append({
            "move_number": move.move_number,
            "move": move.san,
            "best_move": result_before["best_move"],
            "is_best_move": is_best,
            "move_classification": move_classification,
            "best_evaluation": result_before["evaluation"],
            "your_evaluation": result_after["evaluation"],
            "evaluation_change": evaluation_change,
            "evaluation_loss": evaluation_loss,
            "is_critical": is_critical_move,
        })

    return results

