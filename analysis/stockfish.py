import chess
import chess.engine
from models.game import Game
from metrics.move_features import is_best_move, classify_move, is_critical, is_top_3_move, is_top_5_move, is_improvement, is_blunder


STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"


# Starts the Stockfish engine.
def create_engine():
    return chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Analyzes the current position on the board.
def analyze_position(engine, board: chess.Board, perspective: chess.Color):
    results = engine.analyse(
        board,
        chess.engine.Limit(depth = 15),
        multipv = 5
    )

    # Grabs the best move recommended by Stockfish's principal variation (PV).
    best_move = results[0]["pv"][0]

    # Gets the evaluation from the player's perspective (White/Black).
    evaluation = results[0]["score"].pov(perspective)

    # Gets Stockfish's top 3 recommended moves.
    top_3_moves = []

    for result in results:
        top_3_moves.append(result["pv"][0])

        if len(top_3_moves) == 3:
            break

    # Gets Stockfish's top 5 recommended moves.
    top_5_moves = []
    for result in results:
        top_5_moves.append(result["pv"][0])


    return {
        "best_move": best_move,
        "evaluation": evaluation,
        "top_3_moves": top_3_moves,
        "top_5_moves": top_5_moves
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

        # Checks if played move is one of Stockfish's top 5 moves.
        is_top_5 = is_top_5_move(
            board,
            move.san,
            result_before["top_5_moves"]
        )

        # Checks if played move is one of Stockfish's top 3 moves.
        is_top_3 = is_top_3_move(
            board,
            move.san,
            result_before["top_3_moves"]
        )

        # Plays the player's move on the board.
        board.push_san(move.san)

        # Analyzes the position after the move.
        result_after = analyze_position(engine, board, not board.turn)

        # Calculates how much the evaluation changed, in pawns.
        evaluation_change = (
            result_after["evaluation"].score(mate_score = 100000)
            - result_before["evaluation"].score(mate_score = 100000)
        ) / 100

        # Gets the absolute evaluation change.
        evaluation_loss = abs(evaluation_change)

        # Classifies the move based on evaluation loss.
        if is_best:
            move_classification = "best"
        else:
            move_classification = classify_move(evaluation_loss)

        # Checks if the move caused a significant evaluation change.
        is_critical_move = is_critical(evaluation_change)

        # Checks if the player's position improved after the move.
        is_improvement_move = is_improvement(evaluation_change)

        # Checks if the player's move is a blunder.
        is_blunder_move = is_blunder(evaluation_loss)


        results.append({
            "move_number": move.move_number,
            "move": move.san,
            "best_move": result_before["best_move"],
            "is_best_move": is_best,
            "is_top_3_move": is_top_3,
            "is_top_5_move": is_top_5,
            "move_classification": move_classification,
            "best_evaluation": result_before["evaluation"],
            "your_evaluation": result_after["evaluation"],
            "evaluation_change": evaluation_change,
            "evaluation_loss": evaluation_loss,
            "is_critical": is_critical_move,
            "is_improvement": is_improvement_move,
            "is_blunder": is_blunder_move
        })

    return results

