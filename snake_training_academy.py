import pygame, sys, random
from pygame.math import Vector2


class SNAKE():
    def __init__(self,screen=1) -> None:
        self.body = [Vector2(n_cells//2,n_cells//2),Vector2(n_cells//2-1,n_cells//2),Vector2(n_cells//2-2,n_cells//2)]
        self.direction = Vector2(1,0)
        self.screen = screen
        self.limits = self.screen_limits()

    def screen_limits(self):
        if self.screen == 1 :
            return x_gap,x_gap+game_dim,y_gap,y_gap+game_dim
        elif self.screen == 2:
            return x_gap*2+game_dim,2*(x_gap+game_dim),y_gap,y_gap+game_dim

    def draw_snake(self):
        for box in self.body :
            box_rect = pygame.Rect(box.x*cell_size+self.limits[0],box.y*cell_size+self.limits[2],cell_size,cell_size)
            pygame.draw.rect(window,pygame.Color("blue"),box_rect)

    def move_snake(self):
        body_copy = self.body[:]
        body_copy.insert(0,self.body[0]+self.direction)
        self.body = body_copy[:-1]


class FRUIT():
    def __init__(self,screen=1) -> None:
        self.screen = screen
        self.limits = self.screen_limits()
        self.x = random.randint(0,n_cells-1)
        self.y = random.randint(0,n_cells-1)
        self.position = Vector2(self.x,self.y)

    def screen_limits(self):
        if self.screen == 1 :
            return x_gap,x_gap+game_dim,y_gap,y_gap+game_dim
        elif self.screen == 2:
            return x_gap*2+game_dim,2*(x_gap+game_dim),y_gap,y_gap+game_dim

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.limits[0]+self.position.x*cell_size,self.limits[2]+self.position.y*cell_size,cell_size,cell_size)
        pygame.draw.rect(window,pygame.Color("red"),fruit_rect)


class AI():
    def __init__(self,screen = 1) -> None:
        self.screen = screen
        self.score = 0
        self.weights = [0,0,0,0,0,0,0]
        self.snake = SNAKE(screen)
        self.fruit = FRUIT(screen)

    def decide_direction(self):
        while True :
            direction = random.choice([Vector2(1,0),Vector2(-1,0),Vector2(0,1),Vector2(0,-1)])
            if direction + self.snake.body[0] - self.snake.body[1] != Vector2(0,0):
                self.snake.direction = direction
                break


    def update(self):
        self.snake.move_snake()
        self.decide_direction()
        self.check_death()
        self.check_collision()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.position : 
            self.snake.body.insert(0,self.fruit.position)
            while True : 
                self.fruit = FRUIT(self.screen)
                if self.fruit.position not in self.snake.body :
                    break

    def check_death(self):
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

        if self.snake.body[0][0] < 0 or self.snake.body[0][0] > n_cells-1 or self.snake.body[0][1] < 0 or self.snake.body[0][1] > n_cells-1 :
            self.game_over()

    def game_over(self):
        self.snake = SNAKE(self.screen)
        self.fruit = FRUIT(self.screen)


        



    

# settings

dimensions_of_display = (1400,600)

n_cells = 20

n_games = 2 
game_dim = dimensions_of_display[1] - 100
y_gap = (dimensions_of_display[1] - game_dim)//2
x_gap = (dimensions_of_display[0] - game_dim*2)//3
cell_size = game_dim//n_cells
screen_positions = [ (x_gap + (x_gap+game_dim)*x,y_gap) for x in range(n_games)]

game_rects = [pygame.Rect(sp[0],sp[1],game_dim,game_dim) for sp in screen_positions]


pygame.init()

agent1 = AI(1)
agent2 = AI(2)

window = pygame.display.set_mode(dimensions_of_display)

clock = pygame.time.Clock()

# screen update 

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)


#game loop 

while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE :
            agent1.update()
            agent2.update()

    window.fill((230,230,230))

    for game_screen in game_rects :
        pygame.draw.rect(window,(250,190,160),game_screen)

    agent1.draw_elements()
    agent2.draw_elements()


    pygame.display.update()

    clock.tick(60)
