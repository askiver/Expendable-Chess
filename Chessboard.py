import copy
import itertools
import numpy as np
from numpy import ndarray
from dataclasses import dataclass
from operator import attrgetter

from Queen import Queen
from TransTable import TransTable

MAILBOX = np.array([
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, 0, 1, 2, 3, 4, 5, 6, 7, -1,
            -1, 8, 9, 10, 11, 12, 13, 14, 15, -1,
            -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
            -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
            -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
            -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
            -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
            -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

MAILBOX64 = np.array([
            21, 22, 23, 24, 25, 26, 27, 28,
            31, 32, 33, 34, 35, 36, 37, 38,
            41, 42, 43, 44, 45, 46, 47, 48,
            51, 52, 53, 54, 55, 56, 57, 58,
            61, 62, 63, 64, 65, 66, 67, 68,
            71, 72, 73, 74, 75, 76, 77, 78,
            81, 82, 83, 84, 85, 86, 87, 88,
            91, 92, 93, 94, 95, 96, 97, 98])

COLOUR64 = np.array([
	1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0])

PIECES64 = np.array([
	3, 1, 2, 4, 5, 2, 1, 3,
	0, 0, 0, 0, 0, 0, 0, 0,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	0, 0, 0, 0, 0, 0, 0, 0,
	3, 1, 2, 4, 5, 2, 1, 3])

LIGHT = 0
DARK = 1



PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
QUEEN = 4
KING = 5
EMPTY = 6

A1 = 56
B1 = 57
C1 = 58
D1 = 59
E1 = 60
F1 = 61
G1 = 62
H1 = 63

A8 = 0
B8 = 1
C8 = 2
D8 = 3
E8 = 4
F8 = 5
G8 = 6
H8 = 7


SLIDE = np.array([0, 0, 1, 1, 1, 0])

OFFSETS = np.array([0, 8, 4, 4, 8, 8])

OFFSET = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                   [-21, -19, -12, -8, 8, 12, 19, 21],
                   [-11, -9, 9, 11, 0, 0, 0, 0],
                   [-10, -1, 1, 10, 0, 0, 0, 0],
                   [-11, -10, -9, -1, 1, 9, 10, 11],
                   [-11, -10, -9, -1, 1, 9, 10, 11]])

CASTLE_MASK = np.array([7, 15, 15, 15,  3, 15, 15, 11,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	13, 15, 15, 15, 12, 15, 15, 14])

@dataclass
class Move:
    move_from: int
    move_to: int
    bits: int
    score: int = 0
    promote: int = 0

@dataclass
class GameState:
    move: Move
    capture: int
    capture_colour: int
    castle: int
    ep: int
    hash: int
    move_list: list = None


# TODO: Add check for checkmate and stalemate
class Chessboard:

    def __init__(self):

        self.mailbox = MAILBOX
        self.mailbox64 = MAILBOX64
        self.colour = COLOUR64
        self.pieces = PIECES64
        self.ep = -1
        self.castle = 15
        self.side = LIGHT
        self.white_king_pos = E1
        self.black_king_pos = E8
        self.trans_table = TransTable()
        self.hash = self.trans_table.hash(self.side, self.pieces, self.colour, self.ep)

        self.current_available_moves = []
        self.game_history = []

    def row(self, square: int):
        return np.right_shift(square, 3)

    def col(self, square: int):
        return square & 7
        #return np.bitwise_and(square, 7)

    def get_coordinates_from_position(self, position):
        square = self.get_square_from_position(position)
        return square.x_pos, square.y_pos

    def in_check(self, is_black:int):
        for i in range(64):
            if self.pieces[i] == KING and self.colour[i] == is_black:
                return self.attack(i, not is_black)
        return True

    def attack(self, square, is_black:bool):
        for i in range(64):
            if self.colour[i] == is_black:
                if self.pieces[i] == PAWN:
                    column = self.col(i)
                    if not is_black:
                        if column != 0 and i-9 == square:
                            return True
                        if column != 7 and i-7 == square:
                            return True
                    else:
                        if column != 0 and i+7 == square:
                            return True
                        if column != 7 and i+9 == square:
                            return True
                else:
                    for j in range(OFFSETS[self.pieces[i]]):
                        t = i
                        while True:
                            t = self.mailbox[self.mailbox64[t] + OFFSET[self.pieces[i]][j]]
                            if t == -1:
                                break
                            if t == square:
                                return True
                            if self.pieces[t] != EMPTY:
                                break
                            if not SLIDE[self.pieces[i]]:
                                break
        return False

    def generate_moves(self):
        #king_pos = self.white_king_pos if self.side == LIGHT else self.black_king_pos
        for i in range(64):
            if self.colour[i] == self.side:
                if self.pieces[i] == PAWN:
                    column = self.col(i)
                    if self.side == LIGHT:
                        if column != 0 and self.pieces[i-9] != EMPTY:
                            if self.colour[i-9] == DARK or (self.colour[i-9] == LIGHT and self.pieces[i-9] != KING):
                                self.add_move(i, i-9, 17)
                        if column != 7 and self.pieces[i-7] != EMPTY:
                            if self.colour[i-7] == DARK or (self.colour[i-7] == LIGHT and self.pieces[i-7] != KING):
                                self.add_move(i, i-7, 17)
                        if self.pieces[i-8] == EMPTY:
                            self.add_move(i, i-8, 16)
                            if i >= 48 and self.pieces[i-16] == EMPTY:
                                self.add_move(i, i-16, 24)
                    else:
                        if column != 0 and self.pieces[i+7] != EMPTY:
                            if self.colour[i+7] == LIGHT or (self.colour[i+7] == DARK and self.pieces[i+7] != KING):
                                self.add_move(i, i+7, 17)
                        if column != 7 and self.pieces[i+9] != EMPTY:
                            if self.colour[i+9] == LIGHT or (self.colour[i+9] == DARK and self.pieces[i+9] != KING):
                                self.add_move(i, i+9, 17)
                        if self.pieces[i+8] == EMPTY:
                            self.add_move(i, i+8, 16)
                            if i <= 15 and self.pieces[i+16] == EMPTY:
                                self.add_move(i, i+16, 24)
                else:
                    for j in range(OFFSETS[self.pieces[i]]):
                        t = i
                        while True:
                            t = self.mailbox[self.mailbox64[t] + OFFSET[self.pieces[i]][j]]
                            if t == -1:
                                break
                            if self.pieces[t] != EMPTY:
                                if self.colour[t] != self.side:
                                    self.add_move(i, t, 1)
                                else:
                                    if self.pieces[t] != KING:
                                        self.add_move(i, t, 64)
                                break
                            self.add_move(i, t, 0)
                            if not SLIDE[self.pieces[i]]:
                                break
        if self.side == LIGHT:
            if self.castle & 1 != 0:
            #if np.bitwise_and(self.castle, 1):
                self.add_move(E1, G1, 2)
            if self.castle & 2 != 0:
            #if np.bitwise_and(self.castle, 2):
                self.add_move(E1, C1, 2)
        else:
            if self.castle & 4 != 0:
            #if np.bitwise_and(self.castle, 4):
                self.add_move(E8, G8, 2)
            if self.castle & 8 != 0:
            #if np.bitwise_and(self.castle, 8):
                self.add_move(E8, C8, 2)
        if self.ep != -1:
            column = self.col(self.ep)
            if self.side == LIGHT:
                if column != 0 and self.colour[self.ep+7] == LIGHT and self.pieces[self.ep+7] == PAWN:
                    self.add_move(self.ep+7, self.ep, 21)
                if column != 7 and self.colour[self.ep+9] == LIGHT and self.pieces[self.ep+9] == PAWN:
                    self.add_move(self.ep+9, self.ep, 21)
            else:
                if column != 0 and self.colour[self.ep-9] == DARK and self.pieces[self.ep-9] == PAWN:
                    self.add_move(self.ep-9, self.ep, 21)
                if column != 7 and self.colour[self.ep-7] == DARK and self.pieces[self.ep-7] == PAWN:
                    self.add_move(self.ep-7, self.ep, 21)

    def generate_captures_and_promotions(self):
        for i in range(64):
            if self.colour[i] == self.side:
                if self.pieces[i] == PAWN:
                    column = self.col(i)
                    if self.side == LIGHT:
                        if column != 0 and self.colour[i-9] == DARK:
                            self.add_move(i, i-9, 17)
                        if column != 7 and self.colour[i-7] == DARK:
                            self.add_move(i, i-7, 17)
                        if i <= 15 and self.colour[i-8] == EMPTY:
                            self.add_move(i, i-8, 16)

                    else:
                        if column != 0 and self.colour[i+7] == LIGHT:
                            self.add_move(i, i+7, 17)
                        if column != 7 and self.colour[i+9] == LIGHT:
                            self.add_move(i, i+9, 17)
                        if i >= 48 and self.colour[i+8] == EMPTY:
                            self.add_move(i, i+8, 16)
                else:
                    for j in range(OFFSETS[self.pieces[i]]):
                        t = i
                        while True:
                            t = self.mailbox[self.mailbox64[t] + OFFSET[self.pieces[i]][j]]
                            if t == -1:
                                break
                            if self.colour[t] != EMPTY:
                                if self.colour[t] != self.side:
                                    self.add_move(i, t, 1)
                                break
                            if not SLIDE[self.pieces[i]]:
                                break
        if self.ep != -1:
            column = self.col(self.ep)
            if self.side == LIGHT:
                if column != 0 and self.colour[self.ep+7] == LIGHT and self.pieces[self.ep+7] == PAWN:
                    self.add_move(self.ep+7, self.ep, 21)
                if column != 7 and self.colour[self.ep+9] == LIGHT and self.pieces[self.ep+9] == PAWN:
                    self.add_move(self.ep+9, self.ep, 21)
            else:
                if column != 0 and self.colour[self.ep-9] == DARK and self.pieces[self.ep-9] == PAWN:
                    self.add_move(self.ep-9, self.ep, 21)
                if column != 7 and self.colour[self.ep-7] == DARK and self.pieces[self.ep-7] == PAWN:
                    self.add_move(self.ep-7, self.ep, 21)


    def add_move(self, from_square, to_square, flag):
        if flag & 16 != 0:
        #if np.bitwise_and(flag, 16):
            if self.side == LIGHT:
                if to_square <= H8:
                    self.add_promote(from_square, to_square, flag)
                    return
            else:
                if to_square >= A1:
                    self.add_promote(from_square, to_square, flag)
                    return
        move = Move(from_square, to_square, flag)
        if move.bits == 1:
            move.score = 1000 + (self.pieces[to_square] * 10 - self.pieces[from_square])
        elif move.bits == 64:
            move.score = -1
        self.current_available_moves.append(move)

    def add_promote(self, from_square, to_square, flag):
        # TODO add promotion support for other pieces
        #move = Move(from_square, to_square, np.bitwise_or(flag, 32), QUEEN, QUEEN)
        move = Move(from_square, to_square, flag | 32, QUEEN, QUEEN)
        self.current_available_moves.append(move)

    def make_move(self, move):
        if move.bits & 2 != 0:
        #if np.bitwise_and(move.bits, 2):
            if self.in_check(self.side):
                return False
            match move.move_to:
                case 62:
                    if self.colour[F1] != EMPTY or self.colour[G1] != EMPTY or self.attack(F1, not self.side) or self.attack(G1, not self.side):
                        return False
                    move_from = H1
                    move_to = F1
                case 58:
                    if self.colour[B1] != EMPTY or self.colour[C1] != EMPTY or self.colour[D1] != EMPTY or self.attack(C1, not self.side) or self.attack(D1, not self.side):
                        return False
                    move_from = A1
                    move_to = D1
                case 6:
                    if self.colour[F8] != EMPTY or self.colour[G8] != EMPTY or self.attack(F8, not self.side) or self.attack(G8, not self.side):
                        return False
                    move_from = H8
                    move_to = F8
                case 2:
                    if self.colour[B8] != EMPTY or self.colour[C8] != EMPTY or self.colour[D8] != EMPTY or self.attack(C8, not self.side) or self.attack(D8, not self.side):
                        return False
                    move_from = A8
                    move_to = D8
                case _:
                    move_from = -1
                    move_to = -1
            self.colour[move_to] = self.colour[move_from]
            self.pieces[move_to] = self.pieces[move_from]
            self.colour[move_from] = EMPTY
            self.pieces[move_from] = EMPTY


        game_state = GameState(move, self.pieces[move.move_to], self.colour[move.move_to], self.castle, self.ep, self.hash, self.current_available_moves)
        self.game_history.append(game_state)

        self.current_available_moves = []


        #self.castle = np.bitwise_and(self.castle, np.bitwise_and(CASTLE_MASK[move.move_from], CASTLE_MASK[move.move_to]))
        self.castle = CASTLE_MASK[move.move_from] & CASTLE_MASK[move.move_to] & self.castle

        if move.bits & 8 != 0:
        #if np.bitwise_and(move.bits, 8):
            if self.side == LIGHT:
                self.ep = move.move_to + 8
            else:
                self.ep = move.move_to - 8
        else:
            self.ep = -1

        self.colour[move.move_to] = self.side
        if move.bits & 32 != 0:
        #if np.bitwise_and(move.bits, 32):
            self.pieces[move.move_to] = move.promote
        else:
            self.pieces[move.move_to] = self.pieces[move.move_from]
        self.colour[move.move_from] = EMPTY
        self.pieces[move.move_from] = EMPTY

        if move.bits & 4 != 0:
        #if np.bitwise_and(move.bits, 4):
            if self.side == LIGHT:
                self.colour[move.move_to+8] = EMPTY
                self.pieces[move.move_to+8] = EMPTY
            else:
                self.colour[move.move_to-8] = EMPTY
                self.pieces[move.move_to-8] = EMPTY

        #self.side = np.bitwise_xor(self.side, 1)
        self.side ^= 1
        if self.in_check(not self.side):
            self.takeback()
            return False
        self.hash = self.trans_table.hash(self.side, self.pieces, self.colour, self.ep)
        return True

    def takeback(self):

        #self.side = np.bitwise_xor(self.side, 1)
        self.side ^= 1
        game_state = self.game_history.pop()
        move = game_state.move
        capture = game_state.capture
        capture_colour = game_state.capture_colour
        self.castle = game_state.castle
        self.ep = game_state.ep
        self.hash = game_state.hash
        self.current_available_moves = game_state.move_list

        self.colour[move.move_from] = self.side
        #if np.bitwise_and(move.bits, 32):
        if move.bits & 32 != 0:
            self.pieces[move.move_from] = PAWN
        else:
            self.pieces[move.move_from] = self.pieces[move.move_to]
        if capture == EMPTY:
            self.colour[move.move_to] = EMPTY
            self.pieces[move.move_to] = EMPTY
        else:
            self.colour[move.move_to] = capture_colour
            self.pieces[move.move_to] = capture

        if move.bits & 2 != 0:
        #if np.bitwise_and(move.bits, 2):
            match move.move_to:
                case 62:
                    move_from = F1
                    move_to = H1
                case 58:
                    move_from = D1
                    move_to = A1
                case 6:
                    move_from = F8
                    move_to = H8
                case 2:
                    move_from = D8
                    move_to = A8
                case _:
                    move_from = -1
                    move_to = -1
            self.colour[move_to] = self.side
            self.pieces[move_to] = ROOK
            self.colour[move_from] = EMPTY
            self.pieces[move_from] = EMPTY

        if move.bits & 4 != 0:
        #if np.bitwise_and(move.bits, 4):
            if self.side == LIGHT:
                self.colour[move.move_to+8] = self.side ^ 1
                #self.colour[move.move_to+8] = np.bitwise_xor(self.side, 1)
                self.pieces[move.move_to+8] = PAWN
            else:
                self.colour[move.move_to - 8] = self.side ^ 1
                #self.colour[move.move_to-8] = np.bitwise_xor(self.side, 1)
                self.pieces[move.move_to-8] = PAWN

    # Finds move in the list and places it at the front
    def sort_moves(self, move:Move = None):
        self.current_available_moves.sort(key=attrgetter('score'), reverse=True)
        if move is not None:
            for i in range(len(self.current_available_moves)):
                if self.current_available_moves[i] == move:
                    self.current_available_moves.insert(0, self.current_available_moves.pop(i))
                    break


    def share_moves(self):
        move_list = []
        for move in self.current_available_moves:
            if self.make_move(move):
                move_list.append(self.move_to_position(move))
                self.takeback()
        return move_list


    def find_position_from_bitboard(self, position:int):
        column = chr(65 + (position % 8))
        row = 8 - (position // 8)
        return str(column) + str(row)

    def move_to_position(self, move:Move):
        from_position = self.find_position_from_bitboard(move.move_from)
        to_position = self.find_position_from_bitboard(move.move_to)
        return from_position + to_position

    def human_move_piece(self, start_pos, end_pos):
        for move in self.current_available_moves:
            if self.move_to_position(move) == start_pos + end_pos:
                self.make_move(move)
                break

