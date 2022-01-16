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

snake1 = SNAKE()
snake2 = SNAKE(2)
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
            snake1.move_snake()
            snake2.move_snake()

    window.fill((230,230,230))

    for game_screen in game_rects :
        pygame.draw.rect(window,(250,190,160),game_screen)

    snake1.draw_snake()
    snake2.draw_snake()


    pygame.display.update()

    clock.tick(60)
