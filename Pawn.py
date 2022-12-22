from AbstractPiece import AbstractPiece


class Pawn(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('pawn', is_white)

    def valid_moves(self):
        column = self.position[0]
        row = int(self.position[1])
        available_moves = []
        available_moves.append(column + str(row + 1))
        if self.has_moved:
            available_moves.append(column + str(row + 2))
        return available_moves

