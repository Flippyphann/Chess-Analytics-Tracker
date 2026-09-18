import chess.pgn
from io import StringIO
from models.game import Game
from models.move import Move


def parse_game(pgn: str):
    game = chess.pgn.read_game(StringIO(pgn))

    board = game.board()
    moves = []

    for move_number, move in enumerate(game.mainline_moves(), start=1):
        san = board.san(move)
        moves.append(Move(move_number, san))
        board.push(move)

    return Game(
        white=game.headers.get("White", ""),
        black=game.headers.get("Black", ""),
        result=game.headers.get("Result", ""),
        date=game.headers.get("Date", ""),
        time_control=game.headers.get("TimeControl", ""),
        opening=game.headers.get("ECO", ""),
        termination=game.headers.get("Termination", ""),
        moves=moves
    )
