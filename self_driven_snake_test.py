import pygame
from pygame.constants import K_UP
from pygame.math import Vector2
import sys, random


#Game parameters 
num_cells = 30
cell_dimension = 10
speed = 100


class SNAKE:
    def __init__(self) -> None:
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,1)

    def draw_snake(self):
        for square in self.body:
            body_part_rect = pygame.Rect(square.x*cell_dimension,square.y*cell_dimension,cell_dimension,cell_dimension)
            pygame.draw.rect(game_screen,(0,0,255),body_part_rect)

    def move_snake(self):
        body_copy = self.body[:]
        body_copy.insert(0,body_copy[0]+self.direction)
        self.body = body_copy[:-1]

class FRUIT:
    def __init__(self) -> None:
        self.x = random.randint(0,num_cells-1)
        self.y = random.randint(0,num_cells-1)
        self.position = Vector2(self.x,self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.position.x*cell_dimension,self.position.y*cell_dimension,cell_dimension,cell_dimension)
        pygame.draw.rect(game_screen,(255,0,0),fruit_rect)

class GAME :
    def __init__(self) -> None:
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.position :
            self.snake.body.insert(0,self.fruit.position)
            while True : 
                self.fruit = FRUIT()
                if self.fruit.position not in self.snake.body :
                    break
            
    def check_fail(self):
        if self.snake.body[0].x <0 or self.snake.body[0].y <0 or self.snake.body[0].y > num_cells-1 or self.snake.body[0].x > num_cells-1 :
            self.game_over()

        if self.snake.body[0] in self.snake.body[2:]:
            self.game_over()

    def decide_direction(self):
        forbidden_direction = self.snake.body[0] - self.snake.body[1]
        decided_direction = random.choice([Vector2(1,0),Vector2(-1,0),Vector2(0,1),Vector2(0,-1)])
        while True : 
            if decided_direction + forbidden_direction == Vector2(0,0) :
                decided_direction = random.choice([Vector2(1,0),Vector2(-1,0),Vector2(0,1),Vector2(0,-1)])
            else :
                break
        self.snake.direction = decided_direction

    
    def game_over(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()


class AI:
    def __init__(self) -> None:
        self.weights = [ random.random() for x in range(10)]
        self.best_score = -1
        self.game = GAME()
    
    def decide(self):
        return random.random([Vector2(1,0),Vector2(-1,0)])






pygame.init()

# game display

game_screen = pygame.display.set_mode((cell_dimension*num_cells,cell_dimension*num_cells))

game = GAME()
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,speed)

# main game 



# game loop 
while True:
    # check for exit events 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == SCREEN_UPDATE :
            game.update()
    
    game_screen.fill(pygame.Color('green'))
    game.decide_direction()
    game.draw_elements()

    pygame.display.update()

    clock.tick(60)

                