from AbstractPiece import AbstractPiece


class Pawn(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('pawn', is_white, 1)


