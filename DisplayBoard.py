import copy

import numpy as np
import pygame

from BoardSquare import BoardSquare
from chess_pieces.Bishop import Bishop
from chess_pieces.King import King
from chess_pieces.Knight import Knight
from chess_pieces.Pawn import Pawn
from chess_pieces.Queen import Queen
from chess_pieces.Rook import Rook

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLACK_SQUARE = (181, 136, 99)
WHITE_SQUARE = (240, 217, 181)
MOVE_COLOUR = (135, 152, 106)
pygame.mixer.init()

move_sound = pygame.mixer.Sound("sounds/move.mp3")
capture_sound = pygame.mixer.Sound('sounds/capture.mp3')
game_over_sound = pygame.mixer.Sound('sounds/game_over.mp3')


def create_board_square(x_array, y_array, chess_colour, position):
    # Check if the screen is not square, and choose the smallest length
    # divide the smallest dimension by 8 to get the size of each square.
    if SCREEN_WIDTH < SCREEN_HEIGHT or SCREEN_WIDTH == SCREEN_HEIGHT:
        width_height = SCREEN_WIDTH / 8
    else:
        width_height = SCREEN_HEIGHT / 8

    # Finding the top left corner of each square
    x_coordinate = x_array * width_height
    y_coordinate = y_array * width_height

    # Instantiating a board square with the coordinates, width/height, colour and if occupied and its coordinate.
    return BoardSquare(x_coordinate, y_coordinate, width_height, position, None, chess_colour)

def piece_image(square):
    colour = 'w' if square.piece.is_white else 'b'
    image_string = square.piece.piece_type + '_' + colour + '.png'
    return pygame.transform.scale(pygame.image.load("piece_images/" + image_string).convert_alpha(), (100, 100))

class DisplayBoard:
    def __init__(self, screen, chess_board):

        self.screen = screen
        self.chess_board = chess_board
        self.chess_squares = np.zeros(64, dtype=object)
        self.num_pieces = 32
        is_white = False
        for y in range(8):
            is_white = not is_white
            for x in range(8):
                position = chr(x + 65) + str(8 - y)
                self.chess_squares[y * 8 + x] = create_board_square(x, y, is_white, position)
                is_white = not is_white
        

        for square in self.chess_squares:

            if square.position == 'A8' or square.position == 'H8':
                square.piece = Rook(False)

            elif square.position == 'B8' or square.position == 'G8':
                square.piece = Knight(False)

            elif square.position == 'C8' or square.position == 'F8':
                square.piece = Bishop(False)

            elif square.position == 'D8':
                square.piece = Queen(False)

            elif square.position == 'E8':
                square.piece = King(False)

            elif "7" in square.position:
                square.piece = Pawn(False)

            elif "2" in square.position:
                square.piece = Pawn(True)

            elif square.position == 'A1' or square.position == 'H1':
                square.piece = Rook(True)

            elif square.position == 'B1' or square.position == 'G1':
                square.piece = Knight(True)

            elif square.position == 'C1' or square.position == 'F1':
                square.piece = Bishop(True)

            elif square.position == 'D1':
                square.piece = Queen(True)

            elif square.position == 'E1':
                square.piece = King(True)

    def update_board(self):
        for i in range(64):
            if self.chess_board.colour[i] == 6:
                self.chess_squares[i].piece = None
            else:
                self.chess_squares[i].piece = self.bitboard_value_to_piece(self.chess_board.pieces[i], self.chess_board.colour[i])


    def bitboard_value_to_piece(self, bitboard_piece, bitboard_colour):
        if bitboard_colour == 0:
            if bitboard_piece == 0:
                return Pawn(True)
            elif bitboard_piece == 1:
                return Knight(True)
            elif bitboard_piece == 2:
                return Bishop(True)
            elif bitboard_piece == 3:
                return Rook(True)
            elif bitboard_piece == 4:
                return Queen(True)
            elif bitboard_piece == 5:
                return King(True)
        elif bitboard_colour == 1:
            if bitboard_piece == 0:
                return Pawn(False)
            elif bitboard_piece == 1:
                return Knight(False)
            elif bitboard_piece == 2:
                return Bishop(False)
            elif bitboard_piece == 3:
                return Rook(False)
            elif bitboard_piece == 4:
                return Queen(False)
            elif bitboard_piece == 5:
                return King(False)

    def display_piece_moves(self,square):
        start_position = ""
        for squares in self.chess_squares:
            if squares == square:
                start_position = squares.position
                break

        for move in self.chess_board.share_moves():
            if move[:2] == start_position:
                for square in self.chess_squares:
                    if square.position == move[2:]:
                        pygame.draw.circle(self.screen, MOVE_COLOUR,(square.x_pos + square.size / 2, square.y_pos + square.size / 2), 10)

        pygame.display.flip()
        pygame.display.update()

    def display_check(self,position: str):
        for square in self.chess_squares:
            if square.position == position:
                pygame.draw.circle(self.screen, (255, 0, 0),(square.x_pos + square.size / 2, square.y_pos + square.size / 2), 10)
                break



    def display_board(self):
        black_king_pos = None
        white_king_pos = None
        for square in self.chess_squares:
            redraw_surf = pygame.Surface((square.size, square.size))

            if square.is_white:
                redraw_surf.fill(WHITE_SQUARE)
            else:
                redraw_surf.fill(BLACK_SQUARE)

            self.screen.blit(redraw_surf, (square.x_pos, square.y_pos))
            if square.piece is not None:
                if square.piece.piece_type == "king":
                    if square.piece.is_white:
                        white_king_pos = square.position
                    else:
                        black_king_pos = square.position
                self.screen.blit(piece_image(square), (square.x_pos, square.y_pos))

        in_check = self.chess_board.in_check(False)
        if in_check:
            self.display_check(white_king_pos)
        in_check = self.chess_board.in_check(True)
        if in_check:
            self.display_check(black_king_pos)

        pygame.display.flip()
        pygame.display.update()

    def count_pieces(self):
        num_pieces = 0
        for square in self.chess_squares:
            if square.piece is not None:
                num_pieces += 1
        if num_pieces != self.num_pieces:
            self.num_pieces = num_pieces
            return True
        return False

    def play_move_sound(self):
        if self.count_pieces():
            capture_sound.play()
        else:
            move_sound.play()

    def get_square_from_position(self, position:str):
        for square in self.chess_squares:
            if square.position == position:
                return square
        #column = ord(position[0]) - 65
        #row = 8 - int(position[1])
        #return self.chess_squares[column + row*8]

    def get_square_for_position(self, x, y):
        for square in self.chess_squares:
            if square.y_pos < y < square.y_pos + square.size:
                if square.x_pos < x < square.x_pos + square.size:
                    return square