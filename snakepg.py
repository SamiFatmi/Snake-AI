import pygame, sys, random
from pygame.math import Vector2 

class SNAKE : 
    def __init__(self) -> None:
        self.body = [Vector2(10,10),Vector2(11,10),Vector2(12,10)]
        self.direction = Vector2(1,0)
 
    def draw_snake(self):
        for square in self.body:
            square_rect = pygame.Rect(square.x*cell_size,square.y*cell_size,cell_size,cell_size)
            pygame.draw.rect(window,pygame.Color('blue'),square_rect)

    def move_snake(self):
        body_copy = self.body[:]
        body_copy.insert(0,body_copy[0]+self.direction)
        self.body = body_copy[:-1]

class FRUIT : 
    def __init__(self) -> None:
        self.x = random.randint(0,num_cells-1)
        self.y = random.randint(0,num_cells-1)
        self.position = Vector2(self.x,self.y)

    def draw_square(self):
        fruit_rect = pygame.Rect(self.position.x*cell_size,self.position.y*cell_size,cell_size,cell_size )
        pygame.draw.rect(window,pygame.Color('red'),fruit_rect)

#pygame init 
pygame.init()

#window creation 
cell_size = 30
num_cells = 20
window = pygame.display.set_mode((cell_size*num_cells,cell_size*num_cells))

#display rate
clock = pygame.time.Clock()

#objects
fruit = FRUIT()
snake = SNAKE()

#screen update for user input
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

#game loop 
while True : 
    # check for exit events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE :
            snake.move_snake()
    
    # surfaces
    window.fill((138,250,120))
    fruit.draw_square()
    snake.draw_snake()

    # displaying elements 
    pygame.display.update()

    # display rate 
    clock.tick(60)
