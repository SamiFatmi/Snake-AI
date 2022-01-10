import pygame 
from pygame.math import Vector2
from snakepg import window,cell_size,num_cells


class FRUIT : 
    def __init__(self) -> None:
        self.x = 5
        self.y = 5
        self.position = Vector2(self.x,self.y)

    def draw_square(self):
        fruit_rect = pygame.Rect(self.position.x,self.position.y,cell_size,num_cells)
        pygame.draw.rect(window,pygame.Color('red'),fruit_rect)
          

        