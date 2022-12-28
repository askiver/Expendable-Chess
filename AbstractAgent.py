import random


class AbstractAgent:
    def __init__(self, chess_board, is_white):
        self.chess_board = chess_board
        self.is_white = is_white
        self.selected_square = None

    def get_move(self):
        # bad implementation of random move
        while True:
            row = random.randint(1, 8)
            column = random.choice('ABCDEFGH')
            if self.chess_board.check_square_for_piece(column + str(row)):
                self.selected_square = self.chess_board.get_square_from_position(column + str(row))
                if self.selected_square.piece.is_white == self.is_white:
                    if len(self.selected_square.piece.valid_moves) > 0:
                        chosen_move = random.choice(self.selected_square.piece.valid_moves)
                        if not self.chess_board.check_for_self_check(self.is_white,self.selected_square, self.chess_board.get_square_from_position(chosen_move)):
                            return self.selected_square.position, chosen_move