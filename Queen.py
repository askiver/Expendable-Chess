from AbstractPiece import AbstractPiece


class Queen(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('queen', is_white)

    def valid_moves(self):
        return []