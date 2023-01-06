from AbstractPiece import AbstractPiece


class King(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('king', is_white, 0)
