from AbstractPiece import AbstractPiece


class Bishop(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('bishop', is_white, 3)


