import chess.pgn
from io import StringIO
from models.game import Game
from models.move import Move


def parse_game(pgn: str):
    # Reads the PGN.
    game = chess.pgn.read_game(StringIO(pgn))

    # Tracks the board and then stores the moves.
    board = game.board()
    moves = []

    for move_number, move in enumerate(game.mainline_moves(), start=1):
        # Converts the move to Standard Algebraic Notation (SAN).
        san = board.san(move)

        # Stores the move.
        moves.append(Move(move_number, san))

        # Updates the board.
        board.push(move)

    # Creates a Game object.
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
