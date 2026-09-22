from models.move import Move


class Game:
    def __init__(
        self,
        white: str,
        black: str,
        result: str,
        date: str,
        time_control: str,
        opening: str,
        termination: str,
        moves: list[Move]
    ):
        self.white = white
        self.black = black
        self.result = result
        self.date = date
        self.time_control = time_control
        self.opening = opening
        self.termination = termination
        self.moves = moves


