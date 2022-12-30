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
        return value[1], value[2]

    def heuristic(self, board):
        board_evaluation = 0
        for row in board.chess_squares:
            for square in row:
                if square.piece is not None:
                    board_evaluation += square.piece.value
        return [board_evaluation]

    def minimax(self, depth, board, is_white, alpha , beta):
        if depth == 0:
            return self.heuristic(board)

        if is_white:
            value = np.array([-np.inf, None, None])
            for row in board.chess_squares:
                for square in row:
                    if square.piece is not None:
                        if square.piece.is_white:
                            for move in square.piece.valid_moves:
                                copied_list = copy.deepcopy(board.chess_squares)
                                new_board = Chessboard(copied_list, True)
                                new_board.select_square(new_board.get_square_from_position(square.position))
                                new_board.move_piece(move)
                                new_value = self.minimax(depth - 1, new_board, not is_white, alpha, beta)[0]
                                if new_value > value[0]:
                                    value[0] = new_value
                                    value[1] = square.position
                                    value[2] = move
                                if value[0] > beta:
                                    return value
                                alpha = np.max(np.array([alpha, value[0]]))
            return value
        else:
            value = np.array([np.inf, None, None])
            for row in board.chess_squares:
                for square in row:
                    if square.piece is not None:
                        if not square.piece.is_white:
                            for move in square.piece.valid_moves:
                                copied_list = copy.deepcopy(board.chess_squares)
                                new_board = Chessboard(copied_list, True)
                                new_board.select_square(new_board.get_square_from_position(square.position))
                                new_board.move_piece(move)
                                new_value = self.minimax(depth - 1, new_board, not is_white, alpha, beta)[0]
                                if new_value < value[0]:
                                    value[0] = new_value
                                    value[1] = square.position
                                    value[2] = move
                                if value[0] < alpha:
                                    return value
                                beta = np.min(np.array([beta, value[0]]))
            return value


