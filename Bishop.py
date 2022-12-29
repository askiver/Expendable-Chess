from AbstractPiece import AbstractPiece


class Bishop(AbstractPiece):
    def __init__(self, is_white):
        super().__init__('bishop', is_white, 3)


    def valid_moves(self, position):
        column = position[0]
        row = int(position[1])
        available_moves = []
        lower = row
        higher = row

        for i in range(ord(column)+1, ord("J")):
            lower -= 1
            higher += 1
            available_moves.append(chr(i) + str(lower))
            available_moves.append(chr(i) + str(higher))

        lower = row
        higher = row
        for i in range(ord(column)-1, ord("A")-1, -1):
            lower -= 1
            higher += 1
            available_moves.append(chr(i) + str(lower))
            available_moves.append(chr(i) + str(higher))
        for move in available_moves:
            if move[0] not in 'ABCDEFGH' or move[1] not in '12345678':
                available_moves.remove(move)
        return available_moves


