from AbstractPiece import AbstractPiece


class Rook(AbstractPiece):

    def __init__(self, is_white):
        super().__init__('rook', is_white, 5)
