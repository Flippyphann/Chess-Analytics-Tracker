import chess
import chess.engine
from models.game import Game
from metrics.move_features import (is_best_move, classify_move, is_critical, is_top_3_move, is_top_5_move,
is_improvement, is_blunder, is_worsening, is_capture, is_check, is_castle, is_promotion, is_en_passant)


STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"


# Starts the Stockfish engine.
def create_engine():
    return chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Analyzes the current position on the board.


def analyze_position(engine: chess.engine.SimpleEngine, board: chess.Board, perspective: chess.Color) -> dict:
    if board.is_checkmate():
        score = chess.engine.PovScore(chess.engine.Mate(-1), board.turn)
        return {
            "best_move": None,
            "evaluation": score.pov(perspective),
            "top_3_moves": [],
            "top_5_moves": []
        }

    if board.is_game_over():
        score = chess.engine.PovScore(chess.engine.Cp(0), chess.WHITE)
        return {
            "best_move": None,
            "evaluation": score.pov(perspective),
            "top_3_moves": [],
            "top_5_moves": []
        }

    results = engine.analyse(board, chess.engine.Limit(depth=15), multipv=5)

    top_moves: list[chess.Move] = []

    for result in results:
        pv = result.get("pv")
        if pv:
            top_moves.append(pv[0])

    if not top_moves:
        raise RuntimeError("Stockfish returned no candidate moves.")

    return {
        "best_move": top_moves[0],
        "evaluation": results[0]["score"].pov(perspective),
        "top_3_moves": top_moves[:3],
        "top_5_moves": top_moves[:5]
    }

# Analyzes every move in a game.
def analyze_game(engine, game: Game):
    board = chess.Board()
    results = []

    for move in game.moves:

        # Prevents the loop from attempting to analyze moves after the game has ended.
        if board.is_game_over():
            break

        # Analyzes the position before the move.
        result_before = analyze_position(engine, board, board.turn)

        # Checks if played move is best move recommended by engine.
        best_move = result_before["best_move"]

        if best_move is None:
            break

        is_best = is_best_move(board, move.san, best_move)

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

        # Checks if the move is a capture.
        is_capture_move = is_capture(
            board,
            move.san
        )

        # Checks if the move gives check.
        is_check_move = is_check(
            board,
            move.san
        )

        # Checks if the move is a castling move.
        is_castle_move = is_castle(board, move.san)

        # Checks if the given pseudo-legal move is an en passant capture.
        is_en_passant_move = is_en_passant(board, move.san)

        # Checks if the player's move is a promotion.
        is_promotion_move = is_promotion(
            board,
            move.san
        )

        # Plays the player's move on the board.
        board.push_san(move.san)

        # Check whether the move ended the game.
        is_stalemate_game = board.is_stalemate()
        is_insufficient_material_game = board.is_insufficient_material()

        result_after = analyze_position(engine, board, not board.turn)

        # Calculates how much the evaluation changed, in pawns.
        evaluation_change = (
            result_after["evaluation"].score(mate_score = 100000)
            - result_before["evaluation"].score(mate_score = 100000)
        ) / 100

        # Gets how much the player's position worsened.
        evaluation_loss = max(0.0, -evaluation_change)

        # Classifies the move based on evaluation loss.
        if is_best:
            move_classification = "best"
        else:
            move_classification = classify_move(evaluation_loss)

        # Checks if the move caused a significant evaluation change.
        is_critical_move = is_critical(evaluation_change)

        # Checks if the player's position improved after the move.
        is_improvement_move = is_improvement(evaluation_change)

        # Checks if the player's position worsened after the move.
        is_worsening_move = is_worsening(evaluation_change)

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
            "is_worsening": is_worsening_move,
            "is_blunder": is_blunder_move,
            "is_capture": is_capture_move,
            "is_check": is_check_move,
            "is_castle": is_castle_move,
            "is_promotion": is_promotion_move,
            "is_en_passant": is_en_passant_move,
            "is_stalemate": is_stalemate_game,
            "is_insufficient_material": is_insufficient_material_game
        })

    return results

