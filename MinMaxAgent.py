import copy

import numpy as np

from Chessboard import Chessboard

# TODO Add end condition into heuristic function
class MinMaxAgent:
    def __init__(self, depth, chess_board, is_white):
        self.depth = depth
        self.chess_board = chess_board
        self.is_white = is_white

    def get_move(self):
        value = self.minimax(self.depth, self.chess_board, self.is_white, -np.inf, np.inf)
        print("value associated with move: ", value[0])
        return value[1]

    def piece_value(self, piece:int):
        if piece == 0:
            return 1
        elif piece == 1:
            return 3
        elif piece == 2:
            return 3
        elif piece == 3:
            return 5
        elif piece == 4:
            return 9
        elif piece == 5:
            return 100
        return 0


    def heuristic(self):
        piece_bitboard = self.chess_board.pieces
        colour_bitboard = self.chess_board.colour
        value = 0
        for i in range(64):
            if colour_bitboard[i] == 0:
                value += self.piece_value(piece_bitboard[i])
            elif colour_bitboard[i] == 1:
                value -= self.piece_value(piece_bitboard[i])
        return np.array([value, None])

    def minimax(self, depth, board, is_white, alpha , beta):
        if depth == 0:
            return self.heuristic()

        if is_white:
            value = np.array([-np.inf, None])
            self.chess_board.generate_moves()
            for move in self.chess_board.current_available_moves:
                if self.chess_board.make_move(move):
                    new_value = self.minimax(depth - 1, self.chess_board, False, alpha, beta)[0]
                    if new_value > value[0]:
                        value[0] = new_value
                        value[1] = move
                    self.chess_board.takeback()
                    if value[0] >= beta:
                        return value
                    alpha = max(alpha, value[0])
            return value
        else:
            value = np.array([np.inf, None])
            self.chess_board.generate_moves()
            for move in self.chess_board.current_available_moves:
                if self.chess_board.make_move(move):
                    new_value = self.minimax(depth - 1, self.chess_board, True, alpha, beta)[0]
                    if new_value < value[0]:
                        value[0] = new_value
                        value[1] = move
                    self.chess_board.takeback()
                    if value[0] <= alpha:
                        return value
                    beta = min(beta, value[0])
            return value


