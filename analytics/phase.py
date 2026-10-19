import chess


OPENING = "opening"
MIDDLEGAME = "middlegame"
ENDGAME = "endgame"


# Checks whether at least 5 of the 8 minor pieces are developed.
def are_minor_pieces_developed(board: chess.Board) -> bool:
    developed = 0

    original_squares = [
        chess.B1,
        chess.C1,
        chess.F1,
        chess.G1,
        chess.B8,
        chess.C8,
        chess.F8,
        chess.G8
    ]

    for square in original_squares:
        if board.piece_at(square) is None:
            developed += 1

    return developed >= 5


# Counts the number of queens, rooks, knights, and bishops on the board.
def count_non_pawn_pieces(board: chess.Board) -> int:
    count = 0

    for piece in board.piece_map().values():
        if piece.piece_type not in (chess.PAWN, chess.KING):
            count += 1

    return count

# Counts the number of pawns on the board.
def count_pawns(board: chess.Board) -> int:

    return len(board.pieces(chess.PAWN, chess.WHITE)) + \
           len(board.pieces(chess.PAWN, chess.BLACK))


# Checks whether at least 2 non-pawn pieces were removed recently.
def have_significant_pieces_been_exchanged(previous_piece_count: int, current_piece_count: int) -> bool:
    pieces_removed = previous_piece_count - current_piece_count

    return pieces_removed >= 2


# Checks whether at least 2 pawns were removed recently.
def have_significant_pawns_been_exchanged(previous_pawn_count: int, current_pawn_count: int) -> bool:
    pawns_removed = previous_pawn_count - current_pawn_count

    return pawns_removed >= 2

# Checks whether the game should transition from the opening to the middlegame. This is where I define the middlegame.
def should_enter_middlegame(
    board: chess.Board,
    significant_piece_exchanges: bool,
    significant_pawn_changes: bool
) -> bool:

    developed = are_minor_pieces_developed(board)

    if developed:
        return True

    if significant_piece_exchanges and significant_pawn_changes:
        return True

    return False

# Keeps the non-pawn piece counts for the most recent 7 positions.
def update_piece_count_history(history: list[int], current_piece_count: int) -> list[int]:
    history.append(current_piece_count)

    if len(history) > 7:
        history.pop(0)

    return history

# Keeps the pawn counts for the most recent 7 positions.
def update_pawn_count_history(history: list[int],current_pawn_count: int) -> list[int]:
    history.append(current_pawn_count)

    if len(history) > 7:
        history.pop(0)

    return history


# Checks whether at least 2 non-pawn pieces disappeared across the six-ply window.
def had_significant_piece_exchange(
    piece_count_history: list[int]
) -> bool:
    if len(piece_count_history) < 7:
        return False

    return have_significant_pieces_been_exchanged(
        piece_count_history[0],
        piece_count_history[-1]
    )


# Checks whether at least 2 pawns disappeared across the six-ply window.
def had_significant_pawn_exchange(
    pawn_count_history: list[int]
) -> bool:
    if len(pawn_count_history) < 7:
        return False

    return have_significant_pawns_been_exchanged(
        pawn_count_history[0],
        pawn_count_history[-1]
    )
