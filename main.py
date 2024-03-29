import sys
import time

import numpy as np
import pygame

from DisplayBoard import DisplayBoard
from NegaMaxAgent import NegaMaxAgent
from Chessboard import Chessboard


pygame.init()
pygame.font.init()
pygame.mixer.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLACK_SQUARE = (181, 136, 99)
WHITE_SQUARE = (240, 217, 181)
MOVE_COLOUR = (135, 152, 106)

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH), pygame.RESIZABLE)
pygame.display.set_caption("Expendable Chess")

pygame_icon = pygame.image.load('icons/icon2.png')
pygame.display.set_icon(pygame_icon)

clock = pygame.time.Clock()

def get_square_for_position(x, y):
    for row in display_board.chess_squares:
        if row[0].y_pos < y < row[0].y_pos + row[0].size:
            for square in row:
                if square.x_pos < x < square.x_pos + square.size:
                    return square

# Checks if the game is over
# Game is over when a side which is in check has no valid moves
"""
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
    """

chess_board = Chessboard()
display_board = DisplayBoard(screen, chess_board)
chess_board.generate_moves()
display_board.display_board()

first_clicked_square = None
possible_moves = []
white_turn = True
#computer_opponent_random = RandomAgent(chess_board, False)
computer_opponent_minimax = NegaMaxAgent(4, chess_board, False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if not white_turn:
                """
                if check_for_game_over():
                    print("Game Over")
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                                """
                pretime = time.time()
                move = computer_opponent_minimax.get_move()
                print("Time taken: " + str(time.time() - pretime))
                chess_board.make_move(move)
                display_board.update_board()
                display_board.play_move_sound()
                white_turn = True
                display_board.display_board()
            else:
                x, y = pygame.mouse.get_pos()
                clicked_square = display_board.get_square_for_position(x, y)

                # Checking the clicked squares length to determine if first or second click.
                if first_clicked_square is None and clicked_square is not None and clicked_square.piece is not None and clicked_square.piece.is_white == white_turn:
                    # We have a square with a piece and it's the first click
                    first_clicked_square = clicked_square
                    chess_board.generate_moves()

                    #possible_moves = clicked_square.piece.valid_moves(clicked_square.position)
                    #possible_moves = chess_board.find_possible_moves(possible_moves)
                    display_board.display_piece_moves(first_clicked_square)

                elif first_clicked_square is not None and first_clicked_square.position + clicked_square.position in chess_board.share_moves():
                    # We do not have a piece and it's the second click. Move the piece
                    if False:
                        print("Cannot move here. Would put you in check.")
                        first_clicked_square = None
                        display_board.display_board()
                    else:
                        print("Moving", first_clicked_square.piece.piece_type, "From", first_clicked_square.position, "To",
                              clicked_square.position)
                        chess_board.human_move_piece(first_clicked_square.position, clicked_square.position)
                        display_board.update_board()
                        #clicked_square.piece = first_clicked_square.piece
                        #first_clicked_square.piece = None
                        first_clicked_square = None
                        display_board.play_move_sound()
                        white_turn = False
                        display_board.display_board()

                else:
                    # Illegal move was attempted
                    print("Illegal move attempted")
                    first_clicked_square = None
                    display_board.display_board()


    pygame.display.update()
    clock.tick(60)
