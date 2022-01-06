import pygame
import sys
import random

#pygame init 
pygame.init()

#window creation 
window = pygame.display.set_mode((600,600))

#display rate
clock = pygame.time.Clock()



#game loop 
while True : 
    # check for exit events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # surfaces
    window.fill(pygame.Color('green'))

    window.blit(test_surface,(150,150))

    # displaying elements 
    pygame.display.update()

    # display rate 
    clock.tick(60)
