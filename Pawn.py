from AbstractPiece import AbstractPiece


class Pawn(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('pawn', is_white)

    def valid_moves(self, position):
        column = position[0]
        row = int(position[1])
        available_moves = []
        if self.is_white:
            for i in range(3):
                available_moves.append(chr(ord(column)-1+i) + str(row+1))
            if not self.has_moved:
                available_moves.append(column + str(row + 2))
        else:
            for i in range(3):
                available_moves.append(chr(ord(column)-1+i) + str(row-1))
            if not self.has_moved:
                available_moves.append(column + str(row - 2))
        for move in available_moves:
            if move[0] not in 'ABCDEFGH' or move[1] not in '12345678':
                available_moves.remove(move)

        return available_moves

