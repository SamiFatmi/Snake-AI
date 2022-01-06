import pygame
import sys

#pygame init 
pygame.init()

#window creation 
window = pygame.display.set_mode((600,600))

#game loop 
while True : 
    # check for exit events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # displaying elements 
    pygame.display.update()
