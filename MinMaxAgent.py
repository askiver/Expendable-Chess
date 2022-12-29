import copy

from Chessboard import Chessboard


class MinMaxAgent:
    def __init__(self, depth, chess_board, is_white):
        self.depth = depth
        self.chess_board = chess_board
        self.is_white = is_white

    def get_move(self):
        value, start_position, end_position = self.minimax(self.depth, self.chess_board, self.is_white, float("-inf"), float("inf"))
        print("value associated with move: ", value)
        return start_position, end_position

    def heuristic(self, board):
        board_evaluation = 0
        for row in board.chess_squares:
            for square in row:
                if square.piece is not None:
                    board_evaluation += square.piece.value
        return [board_evaluation]

    def minimax(self, depth, board, is_white, alpha , beta ):
        if depth == 0:
            return self.heuristic(board)
        start_position = None
        end_position = None

        if is_white:
            value = float("-inf")
            for row in board.chess_squares:
                for square in row:
                    if square.piece is not None:
                        if square.piece.is_white:
                            for move in square.piece.valid_moves:
                                copied_list = copy.deepcopy(board.chess_squares)
                                new_board = Chessboard(copied_list, True)
                                new_board.select_square(new_board.get_square_from_position(square.position))
                                new_board.move_piece(move)
                                new_value = self.minimax(depth - 1, new_board, False, alpha, beta)[0]
                                if new_value > value:
                                    value = new_value
                                    start_position = square.position
                                    end_position = move
                                if value > beta:
                                    return value, start_position, end_position
                                alpha = max(alpha, value)
            return value, start_position, end_position
        else:
            value = float('inf')
            for row in board.chess_squares:
                for square in row:
                    if square.piece is not None:
                        if not square.piece.is_white:
                            for move in square.piece.valid_moves:
                                copied_list = copy.deepcopy(board.chess_squares)
                                new_board = Chessboard(copied_list, True)
                                new_board.select_square(new_board.get_square_from_position(square.position))
                                new_board.move_piece(move)
                                new_value = self.minimax(depth - 1, new_board, True, alpha, beta)[0]
                                if new_value < value:
                                    value = new_value
                                    start_position = square.position
                                    end_position = move
                                if value < alpha:
                                    return value, start_position, end_position
                                beta = min(beta, value)
            return value, start_position, end_position


