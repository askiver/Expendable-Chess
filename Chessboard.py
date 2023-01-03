import copy
import itertools
import numpy as np
from numpy import ndarray

from Queen import Queen


class Chessboard:
    def __init__(self, chess_squares: ndarray, real_board: bool):
        self.chess_squares = chess_squares
        self.selected_square = None
        self.real_board = real_board

    def get_square_for_position(self, x, y):
        for square in self.chess_squares:
            if square.y_pos < y < square.y_pos + square.size:
                if square.x_pos < x < square.x_pos + square.size:
                    return square

    def get_coordinates_from_position(self, position):
        square = self.get_square_from_position(position)
        return square.x_pos, square.y_pos

    def select_square(self, square):
        self.selected_square = square

    def deselect_square(self):
        self.selected_square = None

    def increment_piece_turns(self):
        for square in self.chess_squares:
            if square.piece is not None:
                if square.piece.has_moved:
                    square.piece.turns_since_move += 1


    # TODO: Add possibility to promote to other pieces than queen
    def move_piece(self, new_square_position):

        new_square = self.get_square_from_position(new_square_position)
        if new_square.position not in self.selected_square.piece.valid_moves:
            self.selected_square = None
            self.legal_moves = []
            return False

        else:
            self.selected_square.piece.move(new_square_position)
            # Castling
            if self.selected_square.piece.piece_type == 'king':
                if abs(ord(self.selected_square.position[0]) - ord(new_square_position[0])) == 2:
                    if new_square_position[0] == 'G':
                        self.get_square_from_position('H' + new_square_position[1]).piece.move('F' + new_square_position[1])
                        self.get_square_from_position('F' + new_square_position[1]).piece = self.get_square_from_position('H' + new_square_position[1]).piece
                        self.get_square_from_position('H' + new_square_position[1]).piece = None
                        self.get_square_from_position('G' + new_square_position[1]).piece = self.selected_square.piece
                    else:
                        self.get_square_from_position('A' + new_square_position[1]).piece.move('D' + new_square_position[1])
                        self.get_square_from_position('D' + new_square_position[1]).piece = self.get_square_from_position('A' + new_square_position[1]).piece
                        self.get_square_from_position('A' + new_square_position[1]).piece = None
                        self.get_square_from_position('C' + new_square_position[1]).piece = self.selected_square.piece
                    self.selected_square.piece = None
                    self.selected_square = None
                    self.update_valid_moves()
                    self.increment_piece_turns()
                    return True


            elif self.selected_square.piece.piece_type == 'pawn':
                if int(new_square_position[1]) == 1 or int(new_square_position[1]) == 8:
                    self.get_square_from_position(new_square_position).piece = Queen(self.selected_square.piece.is_white)
                    self.selected_square.piece = None
                    self.selected_square = None
                    self.update_valid_moves()
                    self.increment_piece_turns()
                    #self.update_valid_moves()
                    #self.increment_piece_turns()
                    return True
                # En passant
                if self.selected_square.position[0] != new_square_position[0]:
                    if self.get_square_from_position(new_square_position).piece is None:
                        movement = 0
                        if self.selected_square.piece.is_white:
                            movement = -1
                        else:
                            movement = 1
                        self.get_square_from_position(new_square_position[0] + str(int(new_square_position[1]) + movement)).piece = None
                        new_square.piece = self.selected_square.piece
                        self.selected_square.piece = None
                        self.selected_square = None
                        self.update_valid_moves()
                        self.increment_piece_turns()
                        #self.update_valid_moves()
                        #self.increment_piece_turns()
                        return True


            new_square.piece = self.selected_square.piece
            self.selected_square.piece = None
            self.selected_square = None
            self.update_valid_moves()
            self.increment_piece_turns()
            #self.update_valid_moves()
            #self.increment_piece_turns()
            return True

    def get_square_from_position(self, position:str):
        column = ord(position[0]) - 65
        row = 8 - int(position[1])
        return self.chess_squares[column + row*8]

    def check_square_for_piece(self, position: str):
        square = self.get_square_from_position(position)
        if square is None:
            return False
        if square.piece is not None:
            return True
        return False

    def find_legal_moves_for_piece(self, piece_type:str, position:str):
        if piece_type == 'pawn':
            return self.find_pawn_moves(position)
        elif piece_type == 'knight':
            return self.find_knight_moves(position)
        elif piece_type == 'rook':
            return self.find_rook_moves(position)
        elif piece_type == 'queen':
            return self.find_queen_moves(position)
        elif piece_type == 'bishop':
            return self.find_bishop_moves(position)
        else:
            return self.find_king_moves(position)

    def update_valid_moves(self):
        for square in self.chess_squares:
            if square.piece is not None:
                piece_type = square.piece.piece_type
                position = square.position
                square.piece.valid_moves = self.find_legal_moves_for_piece(piece_type, position)

        if self.real_board:
            for square in self.chess_squares:
                if square.piece is not None:
                    legal_moves = []
                    for move in square.piece.valid_moves:
                        if not self.check_for_self_check(square.piece.is_white, square, self.get_square_from_position(move)):
                            legal_moves.append(move)
                    square.piece.valid_moves = legal_moves


    def find_pawn_moves(self, position):
        current_square = self.get_square_from_position(position)
        if current_square.piece.is_white:
            movement = 1
        else:
            movement = -1
        column = position[0]
        row = int(position[1])
        move_list = []
        if 1 < row < 8:
            if not self.check_square_for_piece(position[0] + str(int(position[1]) + movement)):
                move_list.append(position[0] + str(int(position[1]) + movement))
        if current_square.piece.has_moved is False:
            if not self.check_square_for_piece(position[0] + str(int(position[1]) + movement * 2)):
                move_list.append(position[0] + str(int(position[1]) + movement * 2))

        if column != 'H':
            if self.check_square_for_piece(chr(ord(position[0]) + 1) + str(int(position[1]) + movement)):
                if self.get_square_from_position(chr(ord(position[0]) + 1) + str(int(position[1]) + movement)).piece.piece_type != 'king':
                    move_list.append(chr(ord(position[0]) + 1) + str(int(position[1]) + movement))
                else:
                    if self.get_square_from_position(chr(ord(position[0]) + 1) + str(int(position[1]) + movement)).piece.is_white != current_square.piece.is_white:
                        move_list.append(chr(ord(position[0]) + 1) + str(int(position[1]) + movement))
            if self.check_square_for_piece(chr(ord(position[0]) + 1) + position[1]):
                piece = self.get_square_from_position(chr(ord(position[0]) + 1) + position[1]).piece
                if piece.piece_type== 'pawn' and piece.en_passant and piece.is_white != current_square.piece.is_white and piece.turns_since_move == 1:
                    move_list.append(chr(ord(position[0]) + 1) + str(int(position[1]) + movement))

        if column != 'A':
            if self.check_square_for_piece(chr(ord(position[0]) - 1) + str(int(position[1]) + movement)):
                piece = self.get_square_from_position(chr(ord(position[0]) - 1) + str(int(position[1]) + movement)).piece
                if piece.piece_type != 'king':
                    move_list.append(chr(ord(position[0]) - 1) + str(int(position[1]) + movement))
                else:
                    if piece.is_white != current_square.piece.is_white:
                        move_list.append(chr(ord(position[0]) - 1) + str(int(position[1]) + movement))

            if self.check_square_for_piece(chr(ord(position[0]) - 1) + position[1]):
                piece = self.get_square_from_position(chr(ord(position[0]) - 1) + position[1]).piece
                if piece.piece_type == 'pawn' and piece.en_passant and piece.turns_since_move == 1 and piece.is_white != current_square.piece.is_white:
                    move_list.append(chr(ord(position[0]) - 1) + str(int(position[1]) + movement))


        return move_list

    def find_knight_moves(self, position):
        column = position[0]
        row = int(position[1])
        available_moves = []
        final_moves = []
        available_moves.append(chr(ord(column) + 1) + str(row + 2))
        available_moves.append(chr(ord(column) + 1) + str(row - 2))
        available_moves.append(chr(ord(column) - 1) + str(row + 2))
        available_moves.append(chr(ord(column) - 1) + str(row - 2))
        available_moves.append(chr(ord(column) + 2) + str(row + 1))
        available_moves.append(chr(ord(column) + 2) + str(row - 1))
        available_moves.append(chr(ord(column) - 2) + str(row + 1))
        available_moves.append(chr(ord(column) - 2) + str(row - 1))
        for move in available_moves:
            if move[0] not in 'ABCDEFGH' or int(move[1:]) not in range(1, 9):
                pass
            else:
                final_moves.append(move)
        final_final_moves = []
        for move in final_moves:
            if self.check_square_for_piece(move):
                if self.get_square_from_position(move).piece.piece_type == 'king':
                    if self.get_square_from_position(move).piece.is_white == self.get_square_from_position(position).piece.is_white:
                        continue
            final_final_moves.append(move)
        return final_final_moves

    def find_rook_moves(self, position):
        new_move_list = []
        for i in range(int(position[1]) + 1, 9):
            if not self.check_square_for_piece(position[0] + str(i)):
                new_move_list.append(position[0] + str(i))
            else:
                if self.get_square_from_position(position[0] + str(i)).piece.piece_type != 'king':
                    new_move_list.append(position[0] + str(i))
                else:
                    if self.get_square_from_position(position[0] + str(i)).piece.is_white != self.get_square_from_position(position).piece.is_white:
                        new_move_list.append(position[0] + str(i))
                break
        for i in range(int(position[1]) - 1, 0, -1):
            if not self.check_square_for_piece(position[0] + str(i)):
                new_move_list.append(position[0] + str(i))
            else:
                if self.get_square_from_position(position[0] + str(i)).piece.piece_type != 'king':
                    new_move_list.append(position[0] + str(i))
                else:
                    if self.get_square_from_position(position[0] + str(i)).piece.is_white != self.get_square_from_position(position).piece.is_white:
                        new_move_list.append(position[0] + str(i))
                break
        for i in range(ord(position[0]) + 1, ord('H') + 1):
            if not self.check_square_for_piece(chr(i) + position[1]):
                new_move_list.append(chr(i) + position[1])
            else:
                if self.get_square_from_position(chr(i) + position[1]).piece.piece_type != 'king':
                    new_move_list.append(chr(i) + position[1])
                else:
                    if self.get_square_from_position(chr(i) + position[1]).piece.is_white != self.get_square_from_position(position).piece.is_white:
                        new_move_list.append(chr(i) + position[1])
                break
        for i in range(ord(position[0]) - 1, ord('A') - 1, -1):
            if not self.check_square_for_piece(chr(i) + position[1]):
                new_move_list.append(chr(i) + position[1])
            else:
                if self.get_square_from_position(chr(i) + position[1]).piece.piece_type != 'king':
                    new_move_list.append(chr(i) + position[1])
                else:
                    if self.get_square_from_position(chr(i) + position[1]).piece.is_white != self.get_square_from_position(position).piece.is_white:
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
                        if square.piece.piece_type == 'king':
                            if square.piece.is_white != self.get_square_from_position(position).piece.is_white:
                                move_list.append(square.position)
                            break
                        move_list.append(square.position)
                        break
                else:
                    break

        for dx in (-1, 1):
            for dy in (-1, 1):
                bishop_moves(dx, dy)
        return move_list


    def find_queen_moves(self, position):
        return self.find_rook_moves(position) + self.find_bishop_moves(position)

    def check_if_in_check(self, is_white):
        king_position = self.find_king_position(is_white)
        for square in self.chess_squares:
            if square.piece:
                if square.piece.is_white != is_white:
                    if king_position in square.piece.valid_moves:
                        return True, king_position
        return False, None

    def find_king_position(self, is_white):
        for square in self.chess_squares:
            if square.piece:
                if square.piece.piece_type == 'king' and square.piece.is_white == is_white:
                    return square.position


    def check_for_self_check(self, is_white, start_square, end_square):
        copied_list = copy.deepcopy(self.chess_squares)
        new_board = Chessboard(copied_list, False)
        new_board.select_square(new_board.get_square_from_position(start_square.position))
        new_board.move_piece(end_square.position)
        in_check = new_board.check_if_in_check(is_white)[0]
        return in_check


    def find_king_moves(self, position):
        column = position[0]
        row = int(position[1])
        available_moves = []
        king = self.get_square_from_position(position).piece
        # Check if king can castle
        if not king.has_moved:
            if not self.check_if_in_check(king.is_white)[0]:
                if self.check_square_for_piece('A' + str(row)):
                    rook_square = self.get_square_from_position('A' + str(row))
                    if rook_square.piece.piece_type == 'rook':
                        if not rook_square.piece.has_moved:
                            if not self.check_square_for_piece('B' + str(row)) and not self.check_square_for_piece('C' + str(row)) and not self.check_square_for_piece('D' + str(row)):
                                if not self.check_for_self_check(king.is_white, self.get_square_from_position(position), self.get_square_from_position('C' + str(row))) and not self.check_for_self_check(king.is_white, self.get_square_from_position(position), self.get_square_from_position('D' + str(row))):
                                    available_moves.append('C' + str(row))
                if self.check_square_for_piece('H' + str(row)):
                    rook_square = self.get_square_from_position('H' + str(row))
                    if rook_square.piece.piece_type == 'rook':
                        if not rook_square.piece.has_moved:
                            if not self.check_square_for_piece('F' + str(row)) and not self.check_square_for_piece('G' + str(row)):
                                if not self.check_for_self_check(king.is_white, self.get_square_from_position(position), self.get_square_from_position('F' + str(row))) and not self.check_for_self_check(king.is_white, self.get_square_from_position(position), self.get_square_from_position('G' + str(row))):
                                    available_moves.append('G' + str(row))


        for i in range(3):
            for j in range(3):
                available_moves.append(chr(ord(column) + i - 1) + str(row + j - 1))
        available_moves.remove(position)
        final_moves = []
        for move in available_moves:
            if move[0] not in 'ABCDEFGH' or move[1] not in '12345678':
                continue
            else:
                final_moves.append(move)
        return final_moves

