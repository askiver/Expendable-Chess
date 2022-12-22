from AbstractPiece import AbstractPiece


class Knight(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('knight', is_white)

    def valid_moves(self, position):
        column = position[0]
        row = int(position[1])
        available_moves = []
        available_moves.append(chr(ord(column)+1) + str(row + 2))
        available_moves.append(chr(ord(column)+1) + str(row - 2))
        available_moves.append(chr(ord(column)-1) + str(row + 2))
        available_moves.append(chr(ord(column)-1) + str(row - 2))
        available_moves.append(chr(ord(column)+2) + str(row + 1))
        available_moves.append(chr(ord(column)+2) + str(row - 1))
        available_moves.append(chr(ord(column)-2) + str(row + 1))
        available_moves.append(chr(ord(column)-2) + str(row - 1))
        for move in available_moves:
            if move[0] not in 'ABCDEFGH' or move[1] not in '12345678':
                available_moves.remove(move)
        return available_moves
