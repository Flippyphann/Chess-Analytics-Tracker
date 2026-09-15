import chess.pgn
from io import StringIO

def parse_game(pgn: str):
    game = chess.pgn.read_game(StringIO(pgn))
    return game

def get_moves(game):
    board = game.board()
    moves = []

    for move in game.mainline_moves():
        moves.append(board.san(move))
        board.push(move)

    return moves