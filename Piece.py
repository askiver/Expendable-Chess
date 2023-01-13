
piece_values_map = {
    "king": 0,
    "queen": 9,
    "rook": 5,
    "pawn": 1,
    "knight": 3,
    "bishop": 3
}

class Piece:
    def __init__(self, piece_type:str, is_white:bool):
        self.piece_type = piece_type
        self.is_white = is_white
        piece_value = piece_values_map[piece_type]
        if self.is_white:
            self.value = piece_value
        else:
            self.value = -piece_value
            