import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()
font = pygame.font.Font('arial.ttf', 25)
screen = pygame.display.set_mode((800, 600))

class Direction(Enum):
    RIGHT = 1
    LEFT  = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', ['x', 'y'])

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass

