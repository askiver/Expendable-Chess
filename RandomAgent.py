import random


class RandomAgent:
    def __init__(self, chess_board, is_white):
        self.chess_board = chess_board
        self.is_white = is_white

    def get_move(self):
        self.chess_board.generate_moves()
        while True:
            chosen_move = random.choice(self.chess_board.current_available_moves)
            if self.chess_board.make_move(chosen_move):
                self.chess_board.takeback()
                return chosen_move