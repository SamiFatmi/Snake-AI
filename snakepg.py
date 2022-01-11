import pygame, sys, random
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN
from pygame.math import Vector2 

class SNAKE : 
    def __init__(self) -> None:
        self.body = [Vector2(12,10),Vector2(11,10),Vector2(10,10)]
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

class MAIN :
    def __init__(self) -> None:
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake() 
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_square()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.position :
            self.snake.body.insert(0,self.fruit.position)
            while True:
                self.fruit = FRUIT()
                if self.fruit.position not in self.snake.body :
                    break
    
    def check_fail(self):
        # check if outside screen 
        if self.snake.body[0].x < 0 or self.snake.body[0].x > num_cells -1 or self.snake.body[0].y < 0 or self.snake.body[0].y > num_cells -1 :
            self.game_over()

        if self.snake.body[0] in self.snake.body[2:] :
            self.game_over()


    def game_over(self):
        pygame.quit()
        sys.exit


#pygame init 
pygame.init()


#window creation 
cell_size = 30
num_cells = 20
window = pygame.display.set_mode((cell_size*num_cells,cell_size*num_cells))

#game 
main_game = MAIN()

#display rate
clock = pygame.time.Clock()

#screen update for user input
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)

#game loop 
while True : 
    # check for exit events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE :
            main_game.update()
        
        if event.type == KEYDOWN : 
            if event.key == K_UP and main_game.snake.direction.y != 1 :
                main_game.snake.direction = Vector2(0,-1)
            if event.key == K_DOWN and main_game.snake.direction.y != -1 :
                main_game.snake.direction = Vector2(0,1)
            if event.key == K_RIGHT and main_game.snake.direction.x != -1 :
                main_game.snake.direction = Vector2(1,0)
            if event.key == K_LEFT and main_game.snake.direction.x != 1 :
                main_game.snake.direction = Vector2(-1,0) 
    
    # surfaces
    window.fill((138,250,120))
    main_game.draw_elements( )

    # displaying elements 
    pygame.display.update()

    # display rate 
    clock.tick(60)
