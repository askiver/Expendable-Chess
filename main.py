import sys
import time

import numpy as np
import pygame

from MinMaxAgent import MinMaxAgent
from RandomAgent import RandomAgent
from Bishop import Bishop
from BoardSquare import BoardSquare
from Chessboard import Chessboard
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook


pygame.init()
pygame.font.init()
pygame.mixer.init()


move_sound = pygame.mixer.Sound("sounds/move.mp3")
capture_sound = pygame.mixer.Sound('sounds/capture.mp3')
game_over_sound = pygame.mixer.Sound('sounds/game_over.mp3')


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLACK_SQUARE = (181, 136, 99)
WHITE_SQUARE = (240, 217, 181)
MOVE_COLOUR = (135, 152, 106)

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Expendable Chess")
clock = pygame.time.Clock()


def piece_image(square):
    colour = 'w' if square.piece.is_white else 'b'
    image_string = square.piece.piece_type + '_' + colour + '.png'
    return pygame.transform.scale(pygame.image.load("piece_images/" + image_string).convert_alpha(), (100, 100))


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


def get_square_for_position(x, y):
    for row in chess_board.chess_squares:
        if row[0].y_pos < y < row[0].y_pos + row[0].size:
            for square in row:
                if square.x_pos < x < square.x_pos + square.size:
                    return square


def redraw_board():
    for square in chess_board.chess_squares:
        redraw_surf = pygame.Surface((square.size, square.size))

        if square.is_white:
            redraw_surf.fill(WHITE_SQUARE)
        else:
            redraw_surf.fill(BLACK_SQUARE)

        screen.blit(redraw_surf, (square.x_pos, square.y_pos))
        if square.piece is not None:
            screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    in_check, position = chess_board.check_if_in_check(True)
    if in_check:
        display_check(position)
    in_check, position = chess_board.check_if_in_check(False)
    if in_check:
        display_check(position)
    pygame.display.flip()
    pygame.display.update()


def display_piece_moves(move_list: list):
    for move in move_list:
        for square in chess_board.chess_squares:
            if square.position == move:
                pygame.draw.circle(screen, MOVE_COLOUR, (square.x_pos + square.size/2, square.y_pos + square.size/2), 10)

    pygame.display.flip()
    pygame.display.update()

def display_check(position:str):
    pos_x, pos_y = chess_board.get_coordinates_from_position(position)
    pygame.draw.circle(screen, (255, 0, 0), (pos_x + 50, pos_y + 50), 10)

white_pieces = []
black_pieces = []
num_white_pieces = 16
num_black_pieces = 16

def count_pieces():
    white_pieces.clear()
    black_pieces.clear()
    for square in chess_board.chess_squares:
        if square.piece is not None:
            if square.piece.is_white:
                white_pieces.append(square.piece)
            else:
                black_pieces.append(square.piece)
# Checks if the game is over
# Game is over when a side which is in check has no valid moves
def check_for_game_over():
    if white_turn:
        for white_piece in white_pieces:
            if white_piece.valid_moves:
                return False
        if chess_board.check_if_in_check(True)[0]:
            print("White has been checkmated")
            return True
        else:
            print("Stalemate")
            return True
    else:
        for black_piece in black_pieces:
            if black_piece.valid_moves:
                return False
        if chess_board.check_if_in_check(False)[0]:
            print("Black has been checkmated")
            return True
        else:
            print("Stalemate")
            return True

def play_move_sound():
    global num_white_pieces, num_black_pieces
    if num_white_pieces > len(white_pieces) or num_black_pieces > len(black_pieces):
        capture_sound.play()
    else:
        move_sound.play()

    num_white_pieces = len(white_pieces)
    num_black_pieces = len(black_pieces)





chess_squares = np.zeros(64, dtype=object)

is_white = False
for y in range(8):
    is_white = not is_white
    for x in range(8):
        position = chr(x + 65) + str(8 - y)
        chess_squares[y * 8 + x] = create_board_square(x, y, is_white, position)
        is_white = not is_white

for square in chess_squares:
    surf = pygame.Surface((square.size, square.size))

    if square.is_white:
        surf.fill((240, 217, 181))
    else:
        surf.fill((181, 136, 99))

    rect = surf.get_rect()
    screen.blit(surf, (square.x_pos, square.y_pos))
    pygame.display.flip()

    if square.position == 'A8' or square.position == 'H8':
        square.piece = Rook(False)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'B8' or square.position == 'G8':
        square.piece = Knight(False)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'C8' or square.position == 'F8':
        square.piece = Bishop(False)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'D8':
        square.piece = Queen(False)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'E8':
        square.piece = King(False)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif "7" in square.position:
        square.piece = Pawn(False)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif "2" in square.position:
        square.piece = Pawn(True)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'A1' or square.position == 'H1':
        square.piece = Rook(True)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'B1' or square.position == 'G1':
        square.piece = Knight(True)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'C1' or square.position == 'F1':
        square.piece = Bishop(True)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'D1':
        square.piece = Queen(True)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))
    elif square.position == 'E1':
        square.piece = King(True)
        screen.blit(piece_image(square), (square.x_pos, square.y_pos))

    if square.piece is not None:
        if square.piece.is_white:
            white_pieces.append(square.piece)
        else:
            black_pieces.append(square.piece)


    pygame.display.flip()

chess_board = Chessboard(chess_squares, True)
chess_board.update_valid_moves()

first_clicked_square = None
possible_moves = []
white_turn = True
computer_opponent_random = RandomAgent(chess_board, False)
computer_opponent_minimax = MinMaxAgent(2, chess_board, False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if not white_turn:
                if check_for_game_over():
                    print("Game Over")
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                pretime = time.time()
                start_pos, end_pos = computer_opponent_minimax.get_move()
                print("Time taken: " + str(time.time() - pretime))
                start_square = chess_board.get_square_from_position(start_pos)
                chess_board.select_square(start_square)
                chess_board.move_piece(end_pos)
                count_pieces()
                play_move_sound()
                white_turn = True
                redraw_board()
            else:
                x, y = pygame.mouse.get_pos()
                clicked_square = chess_board.get_square_for_position(x, y)

                # Checking the clicked squares length to determine if first or second click.
                if first_clicked_square is None and clicked_square is not None and clicked_square.piece is not None and clicked_square.piece.is_white == white_turn:
                    # We have a square with a piece and it's the first click
                    first_clicked_square = clicked_square
                    chess_board.update_valid_moves()
                    chess_board.select_square(clicked_square)
                    #possible_moves = clicked_square.piece.valid_moves(clicked_square.position)
                    #possible_moves = chess_board.find_possible_moves(possible_moves)
                    display_piece_moves(clicked_square.piece.valid_moves)

                elif first_clicked_square is not None and clicked_square.position in first_clicked_square.piece.valid_moves:
                    # We do not have a piece and it's the second click. Move the piece
                    if chess_board.check_for_self_check(first_clicked_square.piece.is_white, first_clicked_square, clicked_square):
                        print("Cannot move here. Would put you in check.")
                        first_clicked_square = None
                        chess_board.deselect_square()
                        redraw_board()
                    else:
                        print("Moving", first_clicked_square.piece.piece_type, "From", first_clicked_square.position, "To",
                              clicked_square.position)
                        chess_board.move_piece(clicked_square.position)
                        #clicked_square.piece = first_clicked_square.piece
                        #first_clicked_square.piece = None
                        first_clicked_square = None
                        count_pieces()
                        play_move_sound()
                        white_turn = False
                        redraw_board()

                else:
                    # Illegal move was attempted
                    print("Illegal move attempted")
                    first_clicked_square = None
                    chess_board.deselect_square()
                    redraw_board()


    pygame.display.update()
    clock.tick(24)
