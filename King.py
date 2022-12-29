from AbstractPiece import AbstractPiece


class King(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('king', is_white, 0)

    def valid_moves(self, position):
        column = position[0]
        row = int(position[1])
        available_moves = []
        for i in range(3):
            for j in range(3):
                available_moves.append(chr(ord(column) + i - 1) + str(row + j - 1))
        available_moves.remove(position)
        for move in available_moves:
            if move[0] not in 'ABCDEFGH' or move[1] not in '12345678':
                available_moves.remove(move)
        return available_moves