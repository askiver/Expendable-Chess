import pygame.image


class AbstractPiece:
    def __init__(self, piece_type:str, is_white:bool):
        self.piece_type = piece_type
        self.is_white = is_white
        self.has_moved = False
        self.is_active = True
        self.valid_moves = []
        self.turns_since_move = -1

    def move(self, new_position:str):
        self.has_moved = True
        self.turns_since_move = 0