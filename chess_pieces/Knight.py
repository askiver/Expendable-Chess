from AbstractPiece import AbstractPiece


class Knight(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('knight', is_white, 3)
