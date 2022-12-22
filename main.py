import pygame

from Bishop import Bishop
from BoardSquare import BoardSquare
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Expendable Chess")
clock = pygame.time.Clock()


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
    for row in chess_board:
        if row[0].y_pos < y < row[0].y_pos + row[0].size:
            for square in row:
                if square.x_pos < x < square.x_pos + square.size:
                    return square


def redraw_board():
    for row in chess_board:
        for square in row:
            redraw_surf = pygame.Surface((square.size, square.size))

            if square.is_white:
                redraw_surf.fill((240, 217, 181))
            else:
                redraw_surf.fill((181, 136, 99))

            screen.blit(redraw_surf, (square.x_pos, square.y_pos))
            if square.piece is not None:
                screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
    pygame.display.flip()
    pygame.display.update()


def display_piece_moves(move_list: list):
    for square in move_list:
        redraw_surf = pygame.Surface((square.size, square.size))
        redraw_surf.fill((0, 255, 0))
        screen.blit(redraw_surf, (square.x_pos, square.y_pos))
    pygame.display.flip()
    pygame.display.update()


chess_board = []
is_white = False
for y in range(8):
    chess_row = []
    is_white = not is_white
    for x in range(8):
        position = chr(x + 65) + str(8 - y)
        chess_row.append(create_board_square(x, y, is_white, position))
        is_white = not is_white
    chess_board.append(chess_row)

for row in chess_board:
    for square in row:
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
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'B8' or square.position == 'G8':
            square.piece = Knight(False)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'C8' or square.position == 'F8':
            square.piece = Bishop(False)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'D8':
            square.piece = Queen(False)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'E8':
            square.piece = King(False)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif "7" in square.position:
            square.piece = Pawn(False)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif "2" in square.position:
            square.piece = Pawn(True)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'A1' or square.position == 'H1':
            square.piece = Rook(True)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'B1' or square.position == 'G1':
            square.piece = Knight(True)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'C1' or square.position == 'F1':
            square.piece = Bishop(True)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'D1':
            square.piece = Queen(True)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))
        elif square.position == 'E1':
            square.piece = King(True)
            screen.blit(square.piece.piece_image, (square.x_pos, square.y_pos))

        pygame.display.flip()

first_clicked_square = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            clicked_square = get_square_for_position(x, y)

            # Checking the clicked squares length to determine if first or second click.
            if first_clicked_square is None and clicked_square.piece is not None:
                # We have a square with a piece and it's the first click
                first_clicked_square = clicked_square
            elif first_clicked_square is not None and clicked_square.piece is not None:
                # We have a piece and it's the second click.
                print("Cannot move here. Space occupied by", clicked_square.piece.piece_type)
                first_clicked_square = None
            elif first_clicked_square is not None and clicked_square.piece is None:
                # We do not have a piece and it's the second click. Move the piece
                print("Moving", first_clicked_square.piece.piece_type, "From", first_clicked_square.position, "To",
                      clicked_square.position)
                clicked_square.piece = first_clicked_square.piece
                first_clicked_square.piece = None
                first_clicked_square = None
                redraw_board()

    pygame.display.update()
    clock.tick(60)
