import pygame, sys, random
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN
from pygame.math import Vector2 
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

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
    def __init__(self,num_cells,cell_size) -> None:
        self.num_cells = num_cells
        self.cell_size = cell_size
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


class Agent: 
    def __init__(self) -> None:
        self.score = 0 
        self.memory = []                
        self.reset()
        

    def reset(self): 
        self.score = 0
        self.memory = []
    
    def get_state(self,game): 
        current_x_direction = game.snake.direction[0]
        current_y_direction = game.snake.direction[1]

        head_x_position = game.snake.body[0][0]
        head_y_position = game.snake.body[0][1]

        fruit_x_position = game.fruit.position[0]
        fruit_y_position = game.fruit.position[1]

        state = [current_x_direction,current_y_direction,head_x_position,head_y_position,fruit_x_position,fruit_y_position]
        
        #get diagonal data 
        diagonal_1 = [] 
        diagonal_2 = [] 
        diagonal_3 = [] 
        diagonal_4 = [] 

        # diagonal 1 : 
        steps = min(head_x_position,head_y_position)
        for x in range(steps): 
            if Vector2(head_x_position-x,head_y_position-x) in game.snake.body : 
                diagonal_1.append(1) 
            elif Vector2(head_x_position-x,head_y_position-x) == game.fruit.position : 
                diagonal_1.append(-1) 
            else: 
                diagonal_1.append(0)
        
        # diagonal 2 : 
        steps = min(head_x_position,game.num_cells -head_y_position)
        for x in range(steps): 
            if Vector2(head_x_position-x,head_y_position+x) in game.snake.body : 
                diagonal_2.append(1) 
            elif Vector2(head_x_position-x,head_y_position+x) == game.fruit.position : 
                diagonal_2.append(-1) 
            else: 
                diagonal_2.append(0)
        
        # diagonal 3 : 
        steps = min(game.num_cells -head_x_position,game.num_cells -head_y_position)
        for x in range(steps): 
            if Vector2(head_x_position+x,head_y_position+x) in game.snake.body : 
                diagonal_3.append(1) 
            elif Vector2(head_x_position+x,head_y_position+x) == game.fruit.position : 
                diagonal_3.append(-1) 
            else: 
                diagonal_3.append(0)

        # diagonal 4 : 
        steps = min(game.num_cells -head_x_position,head_y_position)
        for x in range(steps): 
            if Vector2(head_x_position+x,head_y_position-x) in game.snake.body : 
                diagonal_4.append(1) 
            elif Vector2(head_x_position+x,head_y_position-x) == game.fruit.position : 
                diagonal_4.append(-1) 
            else: 
                diagonal_4.append(0)
        
        state = state + diagonal_1 + diagonal_2 + diagonal_3 + diagonal_4

        return state

    def decide_move(self,game): 
        state = self.get_state(game)
        pass 

    def make_move(self,game,move): 
        game.snake.direction = move 

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
    
    def train_long_memory(self):
        pass 

    



    


        
        
    



#pygame init 
pygame.init()


#window creation 
cell_size = 30
num_cells = 20
window = pygame.display.set_mode((cell_size*num_cells,cell_size*num_cells))

#game 
main_game = MAIN(num_cells,cell_size)

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
    main_game.draw_elements()

    # displaying elements 
    pygame.display.update()

    # display rate 
    clock.tick(60)
