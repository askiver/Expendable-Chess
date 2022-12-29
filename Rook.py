from AbstractPiece import AbstractPiece


class Rook(AbstractPiece):

    def __init__(self, is_white):
        super().__init__('rook', is_white, 5)

    def valid_moves(self, position):
        column = position[0]
        row = int(position[1])
        available_moves = []
        for i in range(8):
            available_moves.append(column + str(i + 1))
            available_moves.append(chr(ord('A') + i) + str(row))
        available_moves = [move for move in available_moves if move != position]
        return available_moves
