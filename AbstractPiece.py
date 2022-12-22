import pygame.image


class AbstractPiece:
    def __init__(self, piece_type:str, is_white:bool):
        self.piece_type = piece_type
        self.is_white = is_white
        self.has_moved = False
        self.is_active = True
        self.piece_image = self.piece_image()

    def move(self, new_position):
        self.position = new_position
        self.has_moved = True

    def piece_image(self):
        colour = 'w' if self.is_white else 'b'
        image_string = self.piece_type + '_' + colour + '.png'
        return pygame.transform.scale(pygame.image.load("piece_images/" + image_string).convert_alpha(), (100, 100))