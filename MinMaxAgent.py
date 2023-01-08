import copy
from dataclasses import dataclass

import numpy as np

from Chessboard import Chessboard, Move

#define DOUBLED_PAWN_PENALTY		10
#define ISOLATED_PAWN_PENALTY		20
#define BACKWARDS_PAWN_PENALTY		8
#define PASSED_PAWN_BONUS			20
#define ROOK_SEMI_OPEN_FILE_BONUS	10
#define ROOK_OPEN_FILE_BONUS		15
#define ROOK_ON_SEVENTH_BONUS		20


#the values of the pieces
piece_value = np.array([100, 300, 300, 500, 900, 0])


#The "pcsq" arrays are piece/square tables. They're values
#added to the material value of the piece based on the
#location of the piece. */

pawn_pcsq = np.array([
	  0,   0,   0,   0,   0,   0,   0,   0,
	  5,  10,  15,  20,  20,  15,  10,   5,
	  4,   8,  12,  16,  16,  12,   8,   4,
	  3,   6,   9,  12,  12,   9,   6,   3,
	  2,   4,   6,   8,   8,   6,   4,   2,
	  1,   2,   3, -10, -10,   3,   2,   1,
	  0,   0,   0, -40, -40,   0,   0,   0,
	  0,   0,   0,   0,   0,   0,   0,   0])

knight_pcsq = np.array([
	-10, -10, -10, -10, -10, -10, -10, -10,
	-10,   0,   0,   0,   0,   0,   0, -10,
	-10,   0,   5,   5,   5,   5,   0, -10,
	-10,   0,   5,  10,  10,   5,   0, -10,
	-10,   0,   5,  10,  10,   5,   0, -10,
	-10,   0,   5,   5,   5,   5,   0, -10,
	-10,   0,   0,   0,   0,   0,   0, -10,
	-10, -30, -10, -10, -10, -10, -30, -10])

bishop_pcsq = np.array([
	-10, -10, -10, -10, -10, -10, -10, -10,
	-10,   0,   0,   0,   0,   0,   0, -10,
	-10,   0,   5,   5,   5,   5,   0, -10,
	-10,   0,   5,  10,  10,   5,   0, -10,
	-10,   0,   5,  10,  10,   5,   0, -10,
	-10,   0,   5,   5,   5,   5,   0, -10,
	-10,   0,   0,   0,   0,   0,   0, -10,
	-10, -10, -20, -10, -10, -20, -10, -10])

king_pcsq = np.array([
	-40, -40, -40, -40, -40, -40, -40, -40,
	-40, -40, -40, -40, -40, -40, -40, -40,
	-40, -40, -40, -40, -40, -40, -40, -40,
	-40, -40, -40, -40, -40, -40, -40, -40,
	-40, -40, -40, -40, -40, -40, -40, -40,
	-40, -40, -40, -40, -40, -40, -40, -40,
	-20, -20, -20, -20, -20, -20, -20, -20,
	  0,  20,  40, -20,   0, -20,  40,  20])

king_endgame_pcsq = np.array([
	  0,  10,  20,  30,  30,  20,  10,   0,
	 10,  20,  30,  40,  40,  30,  20,  10,
	 20,  30,  40,  50,  50,  40,  30,  20,
	 30,  40,  50,  60,  60,  50,  40,  30,
	 30,  40,  50,  60,  60,  50,  40,  30,
	 20,  30,  40,  50,  50,  40,  30,  20,
	 10,  20,  30,  40,  40,  30,  20,  10,
	  0,  10,  20,  30,  30,  20,  10,   0])

#The flip array is used to calculate the piece/square
#values for DARK pieces. The piece/square value of a
#LIGHT pawn is pawn_pcsq[sq] and the value of a DARK
#pawn is pawn_pcsq[flip[sq]]
flip = np.array([
	 56,  57,  58,  59,  60,  61,  62,  63,
	 48,  49,  50,  51,  52,  53,  54,  55,
	 40,  41,  42,  43,  44,  45,  46,  47,
	 32,  33,  34,  35,  36,  37,  38,  39,
	 24,  25,  26,  27,  28,  29,  30,  31,
	 16,  17,  18,  19,  20,  21,  22,  23,
	  8,   9,  10,  11,  12,  13,  14,  15,
	  0,   1,   2,   3,   4,   5,   6,   7])

hash_table_size = 1000000

# TODO: fix so entries used from transposition table are somewhat intelligent

@dataclass
class TableEntry:
    move:Move
    evaluation_score:int
    hash: int
    search_depth: int = np.inf

# TODO Add checkmate condition into heuristic function
class MinMaxAgent:
    def __init__(self, depth, chess_board, is_white):
        self.search_depth = depth
        self.chess_board = chess_board
        self.is_white = is_white
        self.transposition_table = np.zeros(shape=hash_table_size, dtype=TableEntry)
        self.nodes_expanded = 0

    def get_move(self):
        self.nodes_expanded = 0
        value = self.minimax(self.search_depth, self.chess_board, self.is_white, -np.inf, np.inf)
        print("value associated with move: ", value[0])
        print("nodes expanded: ", self.nodes_expanded)
        return value[1]

    def piece_value(self, piece:int):
        if piece == 0:
            return 100
        elif piece == 1:
            return 300
        elif piece == 2:
            return 350
        elif piece == 3:
            return 500
        elif piece == 4:
            return 900
        elif piece == 5:
            return 2000
        return 0

    def piece_position_value(self, piece:int, square:int, colour:int):
        if colour == 0:
            if piece == 0:
                return pawn_pcsq[square]
            elif piece == 1:
                return knight_pcsq[square]
            elif piece == 2:
                return bishop_pcsq[square]
            #elif piece == 3:
                #return rook_pcsq[square]
            #elif piece == 4:
                #return queen_pcsq[square]
            elif piece == 5:
                return king_pcsq[square]
        else:
            if piece == 0:
                return -pawn_pcsq[flip[square]]
            elif piece == 1:
                return -knight_pcsq[flip[square]]
            elif piece == 2:
                return -bishop_pcsq[flip[square]]
            #elif piece == 3:
                #return -rook_pcsq[flip[square]]
            #elif piece == 4:
                #return -queen_pcsq[flip[square]]
            elif piece == 5:
                return -king_pcsq[flip[square]]
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
            value += self.piece_position_value(piece_bitboard[i], i, colour_bitboard[i])
        return np.array([value, None])

    def minimax(self, depth, board, is_white, alpha , beta):
        self.nodes_expanded += 1

        if not depth:
            return self.heuristic()

        table_entry = self.transposition_table[self.chess_board.hash % hash_table_size]

        if table_entry != 0 and table_entry.search_depth < depth and table_entry.hash == self.chess_board.hash:
            return np.array([table_entry.evaluation_score, table_entry.move])

        if is_white:
            value = np.array([-np.inf, None])
            self.chess_board.generate_moves()
            self.chess_board.sort_moves()
            for move in self.chess_board.current_available_moves:
                if self.chess_board.make_move(move):
                    new_value = self.minimax(depth - 1, self.chess_board, False,  alpha, beta)[0]
                    self.chess_board.takeback()
                    if table_entry == 0 or table_entry.evaluation_score < new_value:
                        self.transposition_table[self.chess_board.hash % hash_table_size] = TableEntry(move, new_value, self.chess_board.hash, depth-1)

                    if new_value > value[0]:
                        value[0] = new_value
                        value[1] = move

                    if value[0] >= beta:
                        return value
                    alpha = max(alpha, value[0])
            return value
        else:
            value = np.array([np.inf, None])
            self.chess_board.generate_moves()
            self.chess_board.sort_moves()
            for move in self.chess_board.current_available_moves:
                if self.chess_board.make_move(move):
                    new_value = self.minimax(depth - 1, self.chess_board, True, alpha, beta)[0]
                    self.chess_board.takeback()
                    if table_entry == 0 or table_entry.evaluation_score > new_value:
                        self.transposition_table[self.chess_board.hash % hash_table_size] = TableEntry(move,new_value,self.chess_board.hash,depth-1)

                    if new_value < value[0]:
                        value[0] = new_value
                        value[1] = move

                    if value[0] <= alpha:
                        return value
                    beta = min(beta, value[0])
            return value


