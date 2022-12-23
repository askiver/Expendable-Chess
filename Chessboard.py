import copy
import itertools


class Chessboard:
    def __init__(self, chess_squares: list):
        self.chess_squares = chess_squares
        self.selected_square = None
        self.legal_moves = []

    def get_square_for_position(self, x, y):
        for row in self.chess_squares:
            if row[0].y_pos < y < row[0].y_pos + row[0].size:
                for square in row:
                    if square.x_pos < x < square.x_pos + square.size:
                        return square

    def select_square(self, square):
        self.selected_square = square

    def deselect_square(self):
        self.selected_square = None
        self.legal_moves = []

    def move_piece(self, new_square):
        if not new_square.position in self.legal_moves:
            self.selected_square = None
            self.legal_moves = []
            return False
        else:
            new_square.piece = self.selected_square.piece
            new_square.piece.move()
            self.selected_square.piece = None
            self.selected_square = None
            self.legal_moves = []
            return True

    def get_square_from_position(self, position):
        for row in self.chess_squares:
            for square in row:
                if square.position == position:
                    return square
        return None

    def check_square_for_piece(self, position: str):
        square = self.get_square_from_position(position)
        if square.piece is not None:
            return True
        return False

    def find_possible_moves(self, move_list: list):
        piece_type = self.selected_square.piece.piece_type
        position = self.selected_square.position

        if piece_type == 'pawn':
            self.legal_moves = self.find_pawn_moves(move_list, position)
        elif piece_type == 'knight':
            self.legal_moves = self.find_knight_moves(move_list)
        elif piece_type == 'rook':
            self.legal_moves = self.find_rook_moves(move_list, position)
        elif piece_type == 'queen':
            self.legal_moves = self.find_queen_moves(move_list, position)
        elif piece_type == 'bishop':
            self.legal_moves = self.find_bishop_moves(position)
        else:
            self.legal_moves = move_list
        return self.legal_moves

    def find_pawn_moves(self, move_list, position):
        moves_to_check = [move for move in move_list if move[0] != position[0]]
        for move in moves_to_check:
            if not self.check_square_for_piece(move):
                move_list.remove(move)
            else:
                if self.get_square_from_position(move).piece.piece_type == 'king':
                    move_list.remove(move)
        if self.selected_square.piece.is_white:
            if self.check_square_for_piece(position[0] + str(int(position[1]) + 1)):
                move_list.remove(position[0] + str(int(position[1]) + 1))
        else:
            if self.check_square_for_piece(position[0] + str(int(position[1]) - 1)):
                move_list.remove(position[0] + str(int(position[1]) - 1))
        return move_list

    def find_knight_moves(self, move_list):
        for move in move_list:
            if self.check_square_for_piece(move):
                if self.get_square_from_position(move).piece.piece_type == 'king':
                    move_list.remove(move)
        return move_list

    def find_rook_moves(self, move_list, position):
        new_move_list = []
        for i in range(int(position[1]) + 1, 9):
            if not self.check_square_for_piece(position[0] + str(i)):
                new_move_list.append(position[0] + str(i))
            else:
                if self.get_square_from_position(position[0] + str(i)).piece.piece_type != 'king':
                    new_move_list.append(position[0] + str(i))
                break
        for i in range(int(position[1]) - 1, 0, -1):
            if not self.check_square_for_piece(position[0] + str(i)):
                new_move_list.append(position[0] + str(i))
            else:
                if self.get_square_from_position(position[0] + str(i)).piece.piece_type != 'king':
                    new_move_list.append(position[0] + str(i))
                break
        for i in range(ord(position[0]) + 1, ord('H') + 1):
            if not self.check_square_for_piece(chr(i) + position[1]):
                new_move_list.append(chr(i) + position[1])
            else:
                if self.get_square_from_position(chr(i) + position[1]).piece.piece_type != 'king':
                    new_move_list.append(chr(i) + position[1])
                break
        for i in range(ord(position[0]) - 1, ord('A') - 1, -1):
            if not self.check_square_for_piece(chr(i) + position[1]):
                new_move_list.append(chr(i) + position[1])
            else:
                if self.get_square_from_position(chr(i) + position[1]).piece.piece_type != 'king':
                    new_move_list.append(chr(i) + position[1])
                break
        return new_move_list

    def find_bishop_moves(self, position):

        move_list = []
        def bishop_moves(dx, dy):

            for i in itertools.count(start=1):
                newx = ord(position[0]) - 64 + dx * i
                newy = int(position[1]) + dy * i

                if 0 < newx <= 8 and 0 < newy <= 8:
                    square = self.get_square_from_position(chr(newx + 64) + str(newy))
                    if not self.check_square_for_piece(square.position):
                        move_list.append(square.position)
                    else:
                        if square.piece.piece_type != 'king':
                            move_list.append(square.position)
                        break
                else:
                    break

        for dx in (-1, 1):
            for dy in (-1, 1):
                bishop_moves(dx, dy)
        return move_list


    def find_queen_moves(self, move_list, position):
        return self.find_rook_moves(move_list, position) + self.find_bishop_moves(position)
