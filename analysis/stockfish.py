import chess
import chess.engine
from models.game import Game

STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

def create_engine():
    return chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

def analyze_position(engine, board: chess.Board, perspective: chess.Color):
    result = engine.analyse(
        board,
        chess.engine.Limit(depth=15)
    )

    best_move = result["pv"][0]
    evaluation = result["score"].pov(perspective)

    return {
        "best_move": best_move,
        "evaluation": evaluation
    }

def analyze_game(engine, game: Game):
    board = chess.Board()
    results = []

    for move in game.moves:
        result_before = analyze_position(engine, board, board.turn)

        board.push_san(move.san)

        result_after = analyze_position(engine, board, not board.turn)

        evaluation_loss = abs(
            result_before["evaluation"].score(mate_score=100000)
            - result_after["evaluation"].score(mate_score=100000)
        ) / 100

        results.append({
            "move_number": move.move_number,
            "move": move.san,
            "best_move": result_before["best_move"],
            "best_evaluation": result_before["evaluation"],
            "your_evaluation": result_after["evaluation"],
            "evaluation_loss": evaluation_loss
        })

    return results

