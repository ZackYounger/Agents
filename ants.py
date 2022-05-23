### Zack Younger

import pygame
from copy import deepcopy
import random

# change
pygame.init()

clock = pygame.time.Clock()
fps_limit = 60

background_colour = (0, 0, 0)

width, height = 800, 800
screen = pygame.display.set_mode([width, height])
screen.fill(background_colour)
pygame.display.flip()


class Agent:
    def __init__(self):





running = True
while running:
    clock.tick(fps_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()