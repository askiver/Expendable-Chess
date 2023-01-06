import pygame.image


class AbstractPiece:
    def __init__(self, piece_type:str, is_white:bool, piece_value:int):
        self.piece_type = piece_type
        self.is_white = is_white
        if self.is_white:
            self.value = piece_value
        else:
            self.value = -piece_value