from tracemalloc import Snapshot
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
        self.weights = [-10,1,10,5]
        self.snake = SNAKE(screen)
        self.fruit = FRUIT(screen)

    def decide_direction(self):
        current_direction = self.snake.body[1] - self.snake.body[0]
        directions = [Vector2(1,0),Vector2(-1,0),Vector2(0,1),Vector2(0,-1)]

        available_directions = []
        for direction in directions : 
            if self.snake.body[0][0] + direction[0]<=n_cells-1 and self.snake.body[0][1] + direction[1]<=n_cells-1 and self.snake.body[0][0] + direction[0]>=0 and self.snake.body[0][1] + direction[1]>=0 and self.snake.body[0] + direction not in self.snake.body[1:]:
                available_directions.append(direction)

        directions_scores = []
        if len(available_directions)==1:
            self.snake.direction = available_directions[0]
        else :
            for direction in available_directions : 
                #dangerous_move 
                if self.snake.body[0][0]+direction[0]>n_cells-1 or self.snake.body[0][1]+direction[1]>n_cells-1 or self.snake.body[0][0]+direction[0]<0 or self.snake.body[0][1]+direction[1]<0 or self.snake.body[0]+direction in self.snake.body[2:] :
                    dangerous_move = 1
                else : 
                    dangerous_move = 0 

                #towards_fruit
                if self.snake.body[0][0] == self.fruit.position[0] and direction[0]==0 : 
                    if direction[1] == 1 and self.fruit.position[1] - self.snake.body[0][1] > 0:
                        towards_fruit = 1
                    elif direction[1] == -1 and self.fruit.position[1] - self.snake.body[0][1] < 0:
                        towards_fruit = 1
                    else :
                        towards_fruit = 0
                elif self.snake.body[0][1] == self.fruit.position[1] and direction[1] == 0  :
                    if direction[0] == 1 and self.fruit.position[0] - self.snake.body[0][0] > 0:
                        towards_fruit = 1
                    elif direction[0] == -1 and self.fruit.position[0] - self.snake.body[0][0] < 0:
                        towards_fruit = 1
                    else :
                        towards_fruit = 0
                else :
                    towards_fruit = 0 

                #save_from_danger 
                if self.snake.body[0] + current_direction in self.snake.body[1:] or self.snake.body[0][0]+current_direction[0]>n_cells-1 or self.snake.body[0][1]+current_direction[1]>n_cells-1 or self.snake.body[0][0]+current_direction[0]<0 or self.snake.body[0][1]+current_direction[1]<0 :
                    if not (self.snake.body[0][0]+direction[0]>n_cells-1 or self.snake.body[0][1]+direction[1]>n_cells-1 or self.snake.body[0][0]+direction[0]<0 or self.snake.body[0][1]+direction[1]<0 or self.snake.body[0]+direction in self.snake.body[1:]) :
                        save_from_danger = 1 
                    else : 
                        save_from_danger = 0 
                else : 
                    save_from_danger = 0

                
                #eat the fruit 
                if self.snake.body[0] + direction == self.fruit.position : 
                    eat_fruit = 1
                else:
                    eat_fruit = 0

                score = dangerous_move*self.weights[0] + towards_fruit*self.weights[1] + save_from_danger*self.weights[2] + eat_fruit*self.weights[3]

                directions_scores.append([score,direction])

            if len(directions_scores) == 3 : 
                if directions_scores[0][0] > directions_scores[1][0] :
                    if directions_scores[0][0] > directions_scores[2][0] :
                        self.snake.direction = directions_scores[0][1]
                    else :
                        self.snake.direction = directions_scores[2][1]
                else : 
                    if directions_scores[1][0] > directions_scores[2][0] :
                        self.snake.direction = directions_scores[1][1]
                    else : 
                        self.snake.direction = directions_scores[2][1]
            elif len(directions_scores) == 2 :
                if directions_scores[0][0] > directions_scores[1][0] :
                    self.snake.direction = directions_scores[0][1]
                else : 
                    self.snake.direction = directions_scores[1][1]
            elif len(directions_scores)==1:
                self.snake.direction == directions_scores[0][1]

    


    def update(self):
        self.snake.move_snake()
        self.decide_direction()
        self.check_collision()
        self.check_death()

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
        if self.snake.body[0] in self.snake.body[2:]:
            self.game_over()

        if self.snake.body[0][0] < 0 or self.snake.body[0][0] > n_cells-1 or self.snake.body[0][1] < 0 or self.snake.body[0][1] > n_cells-1 :
            self.game_over()

    def game_over(self):
        self.snake = SNAKE(self.screen)
        self.fruit = FRUIT(self.screen)
        self.weights = [ random.random() for x in range(4)]


        



    

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
pygame.time.set_timer(SCREEN_UPDATE,50)


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
